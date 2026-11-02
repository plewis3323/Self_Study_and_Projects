#!/usr/bin/env python3
"""
ESPN Fantasy Football live-draft assistant.

Reads your league's live draft state straight from ESPN's fantasy API
(picks made so far, your roster, players still on the board) and ranks
the best available players by projected value over replacement, adjusted
for what your roster still needs and whether a player is likely to survive
until your next pick.

Usage:
  draft_assistant.py setup            # verify login, list teams, show roster slots
  draft_assistant.py status           # draft progress, your roster, picks until your turn
  draft_assistant.py best [-n 25] [--pos RB] [--json]   # best available + recommendations
  draft_assistant.py watch [-i 10]    # re-run 'best' whenever a new pick comes in
  draft_assistant.py board            # every pick made so far, by round

Config lives in config.json next to this file (see config.example.json).
"""
import argparse
import json
import os
import sys
import time
from collections import Counter, defaultdict

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.environ.get("FF_CONFIG", os.path.join(HERE, "config.json"))

BASE = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}"
LEAGUE_URL = BASE + "/segments/0/leagues/{league_id}"

POS = {1: "QB", 2: "RB", 3: "WR", 4: "TE", 5: "K", 16: "DST"}
SLOT = {0: "QB", 2: "RB", 3: "RB/WR", 4: "WR", 5: "WR/TE", 6: "TE", 7: "OP",
        16: "DST", 17: "K", 20: "BE", 21: "IR", 23: "FLEX"}
# which positions can fill each flex-type slot
FLEX_ELIG = {3: ["RB", "WR"], 5: ["WR", "TE"], 7: ["QB", "RB", "WR", "TE"],
             23: ["RB", "WR", "TE"]}
PRO_TEAM = {0: "FA", 1: "ATL", 2: "BUF", 3: "CHI", 4: "CIN", 5: "CLE", 6: "DAL", 7: "DEN",
            8: "DET", 9: "GB", 10: "TEN", 11: "IND", 12: "KC", 13: "LV", 14: "LAR",
            15: "MIA", 16: "MIN", 17: "NE", 18: "NO", 19: "NYG", 20: "NYJ", 21: "PHI",
            22: "ARI", 23: "PIT", 24: "LAC", 25: "SF", 26: "SEA", 27: "TB", 28: "WSH",
            29: "CAR", 30: "JAX", 33: "BAL", 34: "HOU"}
INJ = {"ACTIVE": "", "QUESTIONABLE": "Q", "DOUBTFUL": "D", "OUT": "OUT",
       "INJURY_RESERVE": "IR", "SUSPENSION": "SUSP", "PUP": "PUP"}


# ----------------------------------------------------------------------------
# config / http
# ----------------------------------------------------------------------------
def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(f"No config found at {CONFIG_PATH}.\n"
                 f"Copy config.example.json -> config.json and fill in league_id, "
                 f"espn_s2 and swid (see README.md).")
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    for k in ("league_id", "season"):
        if not cfg.get(k):
            sys.exit(f"config.json is missing '{k}'")
    return cfg



def _load_taken():
    path = os.path.join(HERE, "taken.txt")
    names = set()
    if os.path.exists(path):
        for line in open(path):
            line = line.strip().lower()
            if line and not line.startswith("#"):
                names.add(line)
    return names

class ESPN:
    def __init__(self, cfg):
        self.cfg = cfg
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Mozilla/5.0 (draft-assistant)"})
        if cfg.get("espn_s2") and cfg.get("swid"):
            swid = cfg["swid"]
            if not swid.startswith("{"):
                swid = "{" + swid.strip("{}") + "}"
            self.s.cookies.set("espn_s2", cfg["espn_s2"], domain=".espn.com")
            self.s.cookies.set("SWID", swid, domain=".espn.com")
        self.league_url = LEAGUE_URL.format(season=cfg["season"], league_id=cfg["league_id"])

    def _get(self, url, params=None, headers=None):
        r = self.s.get(url, params=params, headers=headers, timeout=30)
        if r.status_code == 401:
            sys.exit("401 Unauthorized: league is private and espn_s2/swid are missing "
                     "or expired. Re-copy the cookies from your browser (see README.md).")
        if r.status_code == 404:
            sys.exit(f"404: league {self.cfg['league_id']} / season {self.cfg['season']} "
                     f"not found. Check league_id and season in config.json.")
        r.raise_for_status()
        return r.json()

    def league(self, views):
        # ESPN wants repeated ?view=a&view=b params
        params = [("view", v) for v in views]
        return self._get(self.league_url, params=params)

    def players(self, limit=600, statuses=("FREEAGENT", "WAIVERS", "ONTEAM")):
        rank_type = self.cfg.get("rank_type") or "PPR"
        flt = {"players": {
            "filterStatus": {"value": list(statuses)},
            "limit": limit,
            "sortDraftRanks": {"sortPriority": 1, "sortAsc": True, "value": rank_type},
            "filterRanksForRankTypes": {"value": [rank_type]},
            "filterStatsForSourceIds": {"value": [1]},          # 1 = projections
            "filterStatsForSplitTypeIds": {"value": [0]},       # 0 = full season
        }}
        data = self._get(self.league_url, params=[("view", "kona_player_info")],
                         headers={"X-Fantasy-Filter": json.dumps(flt)})
        return data.get("players", [])

    def bye_weeks(self):
        try:
            data = self._get(BASE.format(season=self.cfg["season"]),
                             params=[("view", "proTeamSchedules_wl")])
            return {t["id"]: t.get("byeWeek") for t in data["settings"]["proTeams"]}
        except Exception:
            return {}


# ----------------------------------------------------------------------------
# league model
# ----------------------------------------------------------------------------
class Draft:
    def __init__(self, api: ESPN):
        self.api = api
        self.cfg = api.cfg
        raw = api.league(["mSettings", "mTeam", "mRoster", "mDraftDetail"])
        self.raw = raw
        st = raw["settings"]
        self.name = st.get("name", "")
        self.teams = {t["id"]: t for t in raw["teams"]}
        self.members = {m["id"]: m for m in raw.get("members", [])}
        self.n_teams = len(self.teams)
        self.scoring_id = st.get("scoringSettings", {}).get("scoringType")
        ds = st.get("draftSettings", {})
        self.draft_type = ds.get("type", "SNAKE")
        self.pick_order = ds.get("pickOrder") or sorted(self.teams)
        self.auction_budget = ds.get("auctionBudget")
        counts = st.get("rosterSettings", {}).get("lineupSlotCounts", {})
        self.slot_counts = {int(k): v for k, v in counts.items() if v}
        self.roster_size = sum(v for k, v in self.slot_counts.items() if k != 21)
        self.rounds = self.roster_size
        dd = raw.get("draftDetail", {})
        self.drafted = dd.get("drafted", False)
        self.in_progress = dd.get("inProgress", False)
        self.picks = sorted(dd.get("picks", []), key=lambda p: p.get("overallPickNumber", 0))
        self.picked_ids = {p["playerId"] for p in self.picks if p.get("playerId", 0) > 0}
        self.my_team_id = self._find_my_team()
        self.rec_scoring = self._detect_scoring(st)

    # -- identity ---------------------------------------------------------
    def _find_my_team(self):
        tid = self.cfg.get("team_id")
        if tid:
            return int(tid)
        swid = (self.cfg.get("swid") or "").strip("{}").upper()
        if swid:
            for t in self.teams.values():
                for o in t.get("owners", []):
                    if o.strip("{}").upper() == swid:
                        return t["id"]
        return None

    def _detect_scoring(self, st):
        items = st.get("scoringSettings", {}).get("scoringItems", [])
        rec = next((i.get("points", 0) for i in items if i.get("statId") == 53), 0)
        if rec >= 1: return "PPR"
        if rec > 0:  return "Half-PPR"
        return "Standard"

    def team_name(self, tid):
        t = self.teams.get(tid, {})
        n = t.get("name") or f"{t.get('location','')} {t.get('nickname','')}".strip()
        return n or f"Team {tid}"

    # -- starters / needs -------------------------------------------------
    def starter_slots(self):
        """{'QB':1,'RB':2,'WR':2,'TE':1,'FLEX':1,'K':1,'DST':1,...} excluding bench/IR."""
        out = {}
        for sid, n in self.slot_counts.items():
            if sid in (20, 21):
                continue
            out[SLOT.get(sid, str(sid))] = out.get(SLOT.get(sid, str(sid)), 0) + n
        return out

    def team_roster_positions(self, tid):
        """Counter of positions on a team's roster (from draft picks; falls back to mRoster)."""
        c = Counter()
        seen = False
        for p in self.picks:
            if p.get("teamId") == tid and p.get("playerId", 0) > 0:
                seen = True
                pos = self.player_pos.get(p["playerId"])
                if pos: c[pos] += 1
        if not seen:
            for e in self.teams[tid].get("roster", {}).get("entries", []):
                pos = POS.get(e.get("playerPoolEntry", {}).get("player", {}).get("defaultPositionId"))
                if pos: c[pos] += 1
        return c

    def unfilled_starters(self, tid):
        """Greedy fill of starter slots with a team's current roster -> remaining need per slot label."""
        have = self.team_roster_positions(tid).copy()
        need = Counter()
        # dedicated slots first
        for sid, n in self.slot_counts.items():
            if sid in (20, 21) or sid in FLEX_ELIG: continue
            pos = SLOT[sid]
            used = min(have[pos], n)
            have[pos] -= used
            need[pos] += n - used
        # then flex slots
        for sid, n in self.slot_counts.items():
            if sid not in FLEX_ELIG: continue
            for _ in range(n):
                filled = False
                for pos in FLEX_ELIG[sid]:
                    if have[pos] > 0:
                        have[pos] -= 1; filled = True; break
                if not filled:
                    need[SLOT[sid]] += 1
        return need

    # -- pick math (snake) --------------------------------------------------
    def next_pick_number(self):
        return len([p for p in self.picks if p.get("playerId", 0) > 0]) + 1

    def team_for_overall(self, overall):
        n = self.n_teams
        rnd = (overall - 1) // n            # 0-based
        idx = (overall - 1) % n
        if rnd % 2 == 1:
            idx = n - 1 - idx
        return self.pick_order[idx], rnd + 1

    def my_upcoming_picks(self, how_many=3):
        if not self.my_team_id or self.draft_type != "SNAKE":
            return []
        out, o = [], self.next_pick_number()
        total = self.n_teams * self.rounds
        while o <= total and len(out) < how_many:
            tid, rnd = self.team_for_overall(o)
            if tid == self.my_team_id:
                out.append((o, rnd))
            o += 1
        return out

    # -- players ------------------------------------------------------------
    def load_players(self):
        raw = self.api.players()
        byes = self.api.bye_weeks()
        rank_type = self.cfg.get("rank_type") or "PPR"
        self.player_pos = {}
        players = []
        for e in raw:
            p = e.get("player", {})
            pid = p.get("id")
            pos = POS.get(p.get("defaultPositionId"))
            if not pos:
                continue
            self.player_pos[pid] = pos
            proj = 0.0
            for s in p.get("stats", []):
                if s.get("statSourceId") == 1 and s.get("statSplitTypeId") == 0 \
                        and str(s.get("seasonId")) == str(self.cfg["season"]):
                    proj = s.get("appliedTotal", 0.0) or 0.0
            own = p.get("ownership", {}) or {}
            ranks = p.get("draftRanksByRankType", {}) or {}
            rk = ranks.get(rank_type) or ranks.get("PPR") or ranks.get("STANDARD") or {}
            players.append({
                "id": pid, "name": p.get("fullName"), "pos": pos,
                "team": PRO_TEAM.get(p.get("proTeamId"), "?"),
                "bye": byes.get(p.get("proTeamId")),
                "proj": round(proj, 1),
                "adp": round(own.get("averageDraftPosition", 999) or 999, 1),
                "auction": round(own.get("auctionValueAverage", 0) or 0, 1),
                "espn_rank": rk.get("rank", 999),
                "injury": INJ.get(p.get("injuryStatus", "ACTIVE"), p.get("injuryStatus", "")),
                "on_team": e.get("onTeamId", 0),
                "status": e.get("status"),
            })
        # register positions of drafted players not in the pool (rare)
        for pk in self.picks:
            self.player_pos.setdefault(pk.get("playerId"), None)
        self.players = players
        taken_names = _load_taken()
        def _is_taken(pl):
            nm = (pl["name"] or "").lower()
            return any(t in nm or nm in t for t in taken_names)
        self.taken_names = taken_names
        self.available = [pl for pl in players
                          if pl["id"] not in self.picked_ids and not pl["on_team"]
                          and not _is_taken(pl)]
        return self.available

    # -- ranking --------------------------------------------------------------
    def rank_available(self):
        avail = self.available
        starters = self.starter_slots()
        n = self.n_teams

        # league-wide starter demand per position (flex spread across eligible)
        demand = Counter()
        for label, cnt in starters.items():
            if label in POS.values():
                demand[label] += cnt * n
            else:
                elig = next((v for k, v in FLEX_ELIG.items() if SLOT[k] == label), [])
                for pos in elig:
                    demand[pos] += cnt * n / len(elig)
        # subtract what's already been drafted at each position
        drafted_pos = Counter(self.player_pos.get(pid) for pid in self.picked_ids)
        by_pos = defaultdict(list)
        for pl in sorted(avail, key=lambda x: -x["proj"]):
            by_pos[pl["pos"]].append(pl)
        replacement = {}
        for pos, lst in by_pos.items():
            k = max(1, int(round(demand[pos] - drafted_pos[pos])))
            # replacement = first player *after* remaining starter demand is met
            idx = min(k, len(lst) - 1)
            replacement[pos] = lst[idx]["proj"] if lst else 0.0

        my_need = self.unfilled_starters(self.my_team_id) if self.my_team_id else Counter()
        my_have = self.team_roster_positions(self.my_team_id) if self.my_team_id else Counter()
        upcoming = self.my_upcoming_picks(2)
        next_pick = upcoming[0][0] if upcoming else None
        following = upcoming[1][0] if len(upcoming) > 1 else None
        cur_round = (self.next_pick_number() - 1) // n + 1
        late = cur_round >= self.rounds - 2

        for pl in avail:
            pos = pl["pos"]
            vorp = pl["proj"] - replacement.get(pos, 0)
            mult, flags = 1.0, []
            # roster-need adjustments
            if my_need.get(pos, 0) > 0:
                mult *= 1.15; flags.append("NEED")
            elif any(my_need.get(fl, 0) > 0 and pos in FLEX_ELIG[k]
                     for k, fl in SLOT.items() if k in FLEX_ELIG):
                mult *= 1.05; flags.append("flex")
            elif my_have.get(pos, 0) >= starters.get(pos, 0) + 2:
                mult *= 0.75; flags.append("deep")
            if pos in ("K", "DST") and not late:
                mult *= 0.25; flags.append("wait")
            if pl["injury"]:
                flags.append(pl["injury"])
                if pl["injury"] in ("OUT", "IR", "PUP", "SUSP"): mult *= 0.6
            # will they make it back to me?
            if next_pick and following:
                if pl["adp"] < following:   # gone before my *following* pick
                    flags.append("gone-next")
            pl["vorp"] = round(vorp, 1)
            pl["score"] = round(max(vorp, 0) * mult + 0.15 * pl["proj"], 1)
            pl["flags"] = " ".join(flags)
        ranked = sorted(avail, key=lambda x: -x["score"])
        self.replacement = replacement
        return ranked, my_need, upcoming


# ----------------------------------------------------------------------------
# printing
# ----------------------------------------------------------------------------
def hdr(s):
    print(f"\n=== {s} ===")


def print_status(d: Draft):
    hdr(f"{d.name}  ({d.n_teams} teams, {d.rec_scoring}, {d.draft_type} draft)")
    state = "COMPLETE" if d.drafted else ("IN PROGRESS" if d.in_progress else "NOT STARTED")
    print(f"Draft: {state}   picks made: {len(d.picked_ids)}/{d.n_teams * d.rounds}   "
          f"rounds: {d.rounds}")
    print("Starters:", ", ".join(f"{k}x{v}" for k, v in d.starter_slots().items()))
    if d.my_team_id is None:
        print("!! Could not identify your team. Set team_id in config.json "
              "(run 'setup' to list teams).")
        return
    me = d.my_team_id
    print(f"You: {d.team_name(me)} (team_id {me})")
    if d.draft_type == "SNAKE":
        slot = d.pick_order.index(me) + 1 if me in d.pick_order else "?"
        up = d.my_upcoming_picks(3)
        nxt = d.next_pick_number()
        if up:
            gap = up[0][0] - nxt
            msg = "YOU ARE ON THE CLOCK" if gap == 0 else f"{gap} picks until your turn"
            print(f"Draft slot {slot}.  {msg}.  Your next picks: "
                  + ", ".join(f"#{o} (Rd {r})" for o, r in up))
        else:
            print(f"Draft slot {slot}. No picks left for you.")
    else:
        print(f"Auction budget: {d.auction_budget}")
    hdr("Your roster")
    mine = [p for p in d.picks if p.get("teamId") == me and p.get("playerId", 0) > 0]
    byid = {pl["id"]: pl for pl in d.players}
    if not mine:
        print("(empty)")
    for p in mine:
        pl = byid.get(p["playerId"])
        if pl:
            print(f"  Rd{p.get('roundId','?'):>2} #{p.get('overallPickNumber','?'):>3}  "
                  f"{pl['pos']:<3} {pl['name']:<24} {pl['team']:<4} bye {pl['bye'] or '?':<3} "
                  f"proj {pl['proj']:>6}")
        else:
            print(f"  Rd{p.get('roundId','?'):>2}  playerId {p['playerId']} (not in pool)")
    need = d.unfilled_starters(me)
    need_s = ", ".join(f"{k}x{v}" for k, v in need.items() if v) or "none — starters filled"
    print(f"Unfilled starter slots: {need_s}")
    # recent picks / positional runs
    if d.picks:
        recent = [p for p in d.picks if p.get("playerId", 0) > 0][-d.n_teams:]
        runs = Counter(d.player_pos.get(p["playerId"]) for p in recent)
        print("Last round of picks by position:",
              ", ".join(f"{k}:{v}" for k, v in runs.most_common() if k))


def print_best(d: Draft, n=25, pos_filter=None):
    ranked, my_need, upcoming = d.rank_available()
    if pos_filter:
        ranked = [p for p in ranked if p["pos"] == pos_filter.upper()]
    hdr(f"Best available ({len(d.available)} on board)  "
        f"replacement lvl: " + ", ".join(f"{k} {v:.0f}" for k, v in sorted(d.replacement.items())))
    print(f"{'#':>3} {'Pos':<4}{'Player':<24}{'Tm':<4}{'Bye':<4}{'Proj':>6} {'VORP':>6} "
          f"{'ADP':>6} {'ESPN':>5} {'Score':>6}  Flags")
    for i, p in enumerate(ranked[:n], 1):
        print(f"{i:>3} {p['pos']:<4}{p['name'][:23]:<24}{p['team']:<4}{str(p['bye'] or '?'):<4}"
              f"{p['proj']:>6} {p['vorp']:>6} {p['adp']:>6} {p['espn_rank']:>5} "
              f"{p['score']:>6}  {p['flags']}")
    # top-3 by position quick view
    hdr("Top 3 by position")
    by = defaultdict(list)
    for p in ranked:
        if len(by[p["pos"]]) < 3:
            by[p["pos"]].append(p)
    for pos in ("QB", "RB", "WR", "TE", "K", "DST"):
        print(f"  {pos:<4}" + " | ".join(f"{p['name']} ({p['proj']}, ADP {p['adp']})" for p in by[pos]))
    if upcoming:
        print(f"\nFlags: NEED=unfilled starter slot, flex=fills a flex, deep=already stacked, "
              f"wait=K/DST too early, gone-next=ADP says they won't last to your pick after next.")


def print_board(d: Draft):
    byid = {pl["id"]: pl for pl in d.players}
    hdr("Draft board")
    cur = None
    for p in d.picks:
        if p.get("playerId", 0) <= 0: continue
        if p.get("roundId") != cur:
            cur = p.get("roundId"); print(f"-- Round {cur}")
        pl = byid.get(p["playerId"])
        nm = f"{pl['pos']:<3} {pl['name']}" if pl else f"player {p['playerId']}"
        me = " <-- YOU" if p.get("teamId") == d.my_team_id else ""
        print(f"  #{p.get('overallPickNumber'):>3}  {d.team_name(p.get('teamId')):<22} {nm}{me}")


def cmd_setup(cfg):
    api = ESPN(cfg)
    d = Draft(api)
    d.load_players()
    print(f"Connected to '{d.name}' (season {cfg['season']}) — {d.n_teams} teams, "
          f"{d.rec_scoring}, {d.draft_type} draft, {d.rounds} rounds.")
    print("Roster slots:", ", ".join(f"{SLOT.get(k, k)}x{v}" for k, v in d.slot_counts.items()))
    hdr("Teams (set team_id in config.json to yours)")
    for tid in d.pick_order if d.draft_type == "SNAKE" else sorted(d.teams):
        t = d.teams[tid]
        owners = ", ".join(d.members.get(o, {}).get("displayName", o) for o in t.get("owners", []))
        me = "  <-- detected as you" if tid == d.my_team_id else ""
        print(f"  team_id {tid:>2}  {d.team_name(tid):<26} {owners}{me}")
    print(f"\nPlayer pool loaded: {len(d.players)} players, {len(d.available)} available.")
    if d.my_team_id is None:
        print("\n!! Could not auto-detect your team from the SWID cookie — add \"team_id\" to config.json.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    sub.add_parser("status")
    sub.add_parser("board")
    b = sub.add_parser("best")
    b.add_argument("-n", type=int, default=25)
    b.add_argument("--pos")
    b.add_argument("--json", action="store_true", help="dump ranked available players as JSON")
    w = sub.add_parser("watch")
    w.add_argument("-i", type=int, default=10, help="poll interval seconds")
    w.add_argument("-n", type=int, default=15)
    a = ap.parse_args()

    cfg = load_config()
    if a.cmd == "setup":
        return cmd_setup(cfg)
    api = ESPN(cfg)

    def snapshot():
        d = Draft(api); d.load_players(); return d

    if a.cmd == "status":
        print_status(snapshot())
    elif a.cmd == "board":
        print_board(snapshot())
    elif a.cmd == "best":
        d = snapshot()
        if a.json:
            ranked, need, up = d.rank_available()
            if a.pos: ranked = [p for p in ranked if p["pos"] == a.pos.upper()]
            print(json.dumps({"my_team": d.team_name(d.my_team_id) if d.my_team_id else None,
                              "next_pick_overall": d.next_pick_number(),
                              "my_upcoming_picks": up, "unfilled_starters": dict(need),
                              "replacement": d.replacement,
                              "my_roster": [dict(pick=p.get("overallPickNumber"),
                                                 **{k: v for k, v in next((pl for pl in d.players if pl["id"] == p["playerId"]), {}).items()
                                                    if k in ("name", "pos", "team", "bye", "proj")})
                                            for p in d.picks if p.get("teamId") == d.my_team_id and p.get("playerId", 0) > 0],
                              "available": ranked[:a.n]}, indent=1))
        else:
            print_status(d); print_best(d, a.n, a.pos)
    elif a.cmd == "watch":
        last = -1
        while True:
            try:
                d = snapshot()
            except Exception as ex:
                print("fetch error:", ex); time.sleep(a.i); continue
            npk = len(d.picked_ids)
            if npk != last:
                os.system("clear" if os.name != "nt" else "cls")
                print(time.strftime("%H:%M:%S"), f"— {npk} picks made")
                print_status(d); print_best(d, a.n)
                last = npk
                if d.drafted:
                    print("\nDraft complete."); break
            time.sleep(a.i)


if __name__ == "__main__":
    main()
