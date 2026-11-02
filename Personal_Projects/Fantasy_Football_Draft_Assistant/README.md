# ESPN Fantasy Football draft assistant

Pulls your league's **live draft state** from ESPN (picks made, your roster,
players still available with ESPN projections/ADP) and ranks the best
available picks by value-over-replacement, adjusted for your roster needs.

## 1. One-time setup

```bash
cp config.example.json config.json
```

Fill in `config.json`:

| key        | where to get it |
|------------|-----------------|
| `league_id`| the number in your league URL: `fantasy.espn.com/football/league?leagueId=**123456**` |
| `season`   | `2026` |
| `team_id`  | leave `null` first; `setup` prints the list and usually auto-detects you |
| `espn_s2`, `swid` | needed for **private** leagues (almost all are). In Chrome/Edge: open fantasy.espn.com while logged in → F12 → **Application** tab → Cookies → `https://fantasy.espn.com` → copy the values of `espn_s2` (long string) and `SWID` (`{XXXXXXXX-...}`). Firefox: F12 → Storage → Cookies. |
| `rank_type`| `PPR`, `STANDARD` — which ESPN ranking to pull (projections are league-scored either way) |

Then verify:

```bash
python3 ~/Personal_Projects/fantasy_draft/draft_assistant.py setup
```

If it can't auto-detect your team, copy your `team_id` from the printed list into `config.json`.

`config.json` contains login cookies — it's git-ignored; never commit or share it.
The cookies expire after a while; if you get a 401, re-copy them.

## 2. On draft day

```bash
python3 ~/Personal_Projects/fantasy_draft/draft_assistant.py status      # picks made, your roster, picks until you're up
python3 ~/Personal_Projects/fantasy_draft/draft_assistant.py best -n 30  # ranked best available + top 3 per position
python3 ~/Personal_Projects/fantasy_draft/draft_assistant.py best --pos RB
python3 ~/Personal_Projects/fantasy_draft/draft_assistant.py board       # every pick so far
python3 ~/Personal_Projects/fantasy_draft/draft_assistant.py watch -i 8  # auto-refresh whenever a new pick comes in
```

Or just open Claude Code and use `/ff-draft` (e.g. `/ff-draft who should I take?`) —
it runs the script and reasons over the live board with you.

## How the ranking works

* **Proj** – ESPN's season projection under your league's scoring.
* **VORP** – projection minus the *replacement level* at that position: the
  projection of the player who would be left once every team's remaining
  starter slots at that position are filled (flex demand split across RB/WR/TE).
  This is what makes an RB2 worth more than a QB with a higher raw number.
* **Score** – VORP × need multiplier (+15% if it fills one of your empty starter
  slots, −25% if you're already 2-deep, K/DST heavily discounted until the last
  3 rounds, injured players discounted) + a small projection term as tiebreak.
* **gone-next** – ADP says the player won't survive until your pick *after* next,
  i.e. take them now or lose them.

Treat it as a strong second opinion, not gospel — it doesn't know about bye-week
stacking, handcuffs, or your league-mates' tendencies. That's what the chat is for.

## Notes / limits

* Works for **snake** drafts fully; auction drafts get status/best-available with
  ESPN auction values but no bidding logic.
* ESPN **mock drafts** are not exposed through the league API, so this only works
  for your real league draft (and for reviewing it afterwards).
* Endpoint: `lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/...` (unofficial; if
  ESPN changes it, update `BASE` at the top of the script).
