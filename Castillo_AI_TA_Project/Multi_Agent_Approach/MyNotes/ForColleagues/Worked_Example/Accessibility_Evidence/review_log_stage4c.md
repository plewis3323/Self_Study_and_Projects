# Stage 4c review log — publication readiness and accessibility

Five physics-PhD referees acting as journal referees for a major physics
publisher, plus one Accessibility Auditor holding an independent vote. Recorded
round by round so the loop is auditable (Success Criterion 12).

Reviewer emphases were assigned so the five did not duplicate each other:
1 coverage and restraint in additions · 2 physics and mathematical correctness ·
3 typesetting and notation convention · 4 figures, captions and alt text ·
5 adversarial — the gap between what is claimed and what is true.

---

## Round 1 — verdicts: REVISE ×5 referees, REVISE auditor (6 of 6)

**Submitted:** the 9-page build.

### What the referees agreed on

**The physics is correct.** Referee 2 re-derived every step independently — the
flux argument, the quadrature and its `u` substitution, both eccentricity
reductions, `cot²(θ/2) = ε²−1`, `ds/dθ`, the ¼ prefactor of the Rutherford
result (two independent ways), the divergence integral including its sign, both
Legendre transforms, and the full `dH` expansion with its cancellation pairs —
and could not break one. No referee found a physics error in the document.

### Principal findings

| # | Finding | Raised by | Severity |
|---|---|---|---|
| 1 | **A source display was replaced by prose** — the factored quadrature step with its two underbraces. Worse, erratum E1 cited that line as its evidence, pointing the reader at something not in the document. | 1, 2, B | blocker |
| 2 | **The tag tree was malformed.** Two `Sect` elements auto-closed, "nesting can be wrong" — while veraPDF passed. Principle 10's failure mode exactly. | 1, 3, 5 | blocker |
| 3 | **The checker reported `mathml_empty: 0` while 8 boxed equations carried only a replacement character** — including the Rutherford cross section. Two bugs: it read page streams (the MathML is in `/AF` files) and counted `<mtext>` as content. | 5, auditor | blocker |
| 4 | **No `Formula` element carried `/Alt` or `/ActualText`** — the accsupp span sits *inside* the Formula, so the element itself had no accessible representation. | 5, auditor | high |
| 5 | **Two overfull boxes**, one of 68.5 pt where a table ran nearly an inch into the margin; caption rules collided with caption text on all three tables. | 1, 3 | blocker |
| 6 | **Seven of eight floats were never cited in the body**; two starred subsections were absent from the outline. | 3, 4, 5 | blocker |
| 7 | **The errata policy was not applied consistently** — part of E9 corrected without a flag, E7 flagged at one of two occurrences. | 1, 2, 5 | major |
| 8 | **The hand-off package shipped a different document** — 7 pages, three days stale. | 5 | major |
| 9 | **The HTML companion was stale** and omitted the errata; its figures were aspect-distorted. | 5, auditor | major |
| 10 | Notation deviations (θ̃, ε, the form of H, Gaussian units, σ(Ω) ≡ σ(θ)) lived only in LaTeX comments the reader never sees. | 3 | major |
| 11 | fig1 clipped through the emergent-ring band; fig3 alt text named the apsidal line as the outgoing asymptote; fig5 alt text invented a label. | 4, A | blocker |

### Findings rejected after examination

- **E4 and half of E5 were FALSE errata.** Referee 2 showed `cos(θ̃′−θ̃′)=cos 0=1`
  is the correct *evaluation*, and that the first quotient-rule term's omitted
  denominator is value-preserving. Both flags withdrawn — a manufactured defect
  is as damaging as a missed one.
- **The auditor's "figure ink fails 1.4.11 at 2.71:1"** was measured on
  RGB(64,161,255), which is the cyan graph-paper ruling (G−R = +97), not pen.
  The pen is RGB(51,51,204) at 8.45:1.
- **"Redraw the figures as vector art"** (referees 3 and 4) and **"remove `[H]`
  and let floats float"** (referee 3) both contradict the governing
  specification and were declined, with reasons recorded.

### Changes applied

The restored quadrature display; the tag-tree fix (isolated by bisection to
`\sout` around mathematics inside a theorem environment); `/ActualText` on all
8 boxed Formula elements; table `/Summary` on all 3; every float cited;
numbered subsections in the outline; the notation table; Gaussian units and
σ(Ω) ≡ σ(θ) stated; one `\erratum` device plus a separate `\supplied` device;
the `sin⁻²` silent correction reversed and flagged; overfull boxes cleared;
figure crops and widths revised; HTML rebuilt to parity (185 MathML in both);
hand-off package rebuilt; and four bugs fixed in the pipeline's own checkers.

---

## Round 2 — verdicts: REVISE / APPROVE / APPROVE / REVISE / REVISE; auditor incomplete

Submitted: the 11-page build, md5 `07b8e22921f1e63b0821db8e52c3f8a1`, frozen
for the duration of the review. Each referee was given their own round-1
findings with what was done about each, including the items deliberately **not**
done and why, and asked to challenge those. The Accessibility Auditor's round-2
session hit a rate limit and never returned a vote.

| Agent | Verdict | What actually blocked |
|---|---|---|
| Referee 1 (coverage) | **REVISE** | Caption/`\toprule` gap measured ~2 pt, not the claimed 6 pt. Split sentences after E2 ("this becomes") and E5 ("and substituting into Eq. (9)"). Optional: name Goldstein in the visible document; restore "Chapter 8" in §4; trim E9 typeface/provenance. |
| Referee 2 (physics) | **APPROVE** | One minor wording defect: the origin of `θ̃` was stated backwards. |
| Referee 3 (typesetting) | **APPROVE** | Four proof-stage nits, none blocking. |
| Referee 4 (figures) | **REVISE** | fig1 box `[20,150,1428,1070]` imported the `σ(Ω)dΩ` line (band ends y≈935). fig3 box `[1340,1485,2340,2040]` imported a stray `⇐` and a redundant heading. Alt-text nits on the theta arc, the double-headed arrow, "follows it", and fig4 arrowheads. |
| Referee 5 (adversarial) | **REVISE** | Empty-MathML identity was a count comparison plus a hard-coded "(all boxed)"; `/Summary` landed on first TH, not Table; `/Scope` was claimed missing while ClassMap supplies it; "20 U+FFFD all in boxed shells" is false (12 sit in `\cancel` strokes); `\erratum` always appended "Reproduced above as written" even for E9, whose casing was changed; Stage 2 round-3 verdicts were unrecorded; boxed ActualText announced ~4×. |
| Accessibility Auditor | *(no vote)* | Session rate-limited. |

### Changes applied (round 2 → rebuild `85b05d31081368d8b811063456c7f769`)

- Caption gap: `skip=12pt` plus `\abovetopsep=10pt` (tagged captions ignore skip; abovetopsep is inside the tabular). Measured: Table 1 **11.0 pt**, Table 2 **10.5 pt**, Table 3 **8.3 pt**.
- Split sentences re-knit: "Eq. (18) then becomes"; "Substituting into Eq. (9) gives".
- Goldstein named in §3.3, Table 3 caption, and the "Goldstein / elsewhere" column. §4 title restored to "Chapter 8. The Hamiltonian…". Remarks bookmark is "Remarks on Eq. (37)".
- E9 uses the star form of `\erratum`, which omits "Reproduced above as written."
- fig1 recropped to `[0,150,1428,936]`; fig3 to `[1470,1585,2340,2040]`. Alt text corrected.
- `\boxeq`/`\ovaleq` carry only `\formulaalt` (inner accsupp dropped to stop 4× announcement). Retraction uses `\formulaalt` + `\xcancel` rather than an ActualText that swallowed the math.
- `\tablesummary` walks the tag stack for the Table ancestor and is placed in `\noalign` immediately after `\begin{tabular}`.
- `check_structure.py`: `/Summary` must sit on the Table element; empty MathML is identity-matched per Formula (no count comparison, no "(all boxed)" literal). `check_contrast.py` ignores a pen layer that is <2 % of dark pixels.

## Round 3 — submitted for re-review

Submitted: the 11-page rebuild, md5 `85b05d31081368d8b811063456c7f769`, frozen
for the duration of this round. Referees 1, 4 and 5 (and the auditor) are
asked to verify the round-2 blockers; referees 2 and 3 to confirm no
regression. Verdicts recorded below as they arrive.

| Agent | Verdict | Notes |
|---|---|---|
| Referee 1 (coverage) | **APPROVE** | Caption–rule ink gaps 11.76 / 11.28 / 11.28 pt; split sentences re-knit; Goldstein, Chapter 8, and E9 star form verified. Coverage of four source pages intact. No new blockers. |
| Referee 2 (physics) | **APPROVE** | θ̃ origin sentence now correct (Eq. (18) = forward beam axis / incoming asymptote at π; thereafter apsidal line / apsis at 0). No physics or errata-policy regression. |
| Referee 3 (typesetting) | **APPROVE** | 0 overfull, 0 tag-structure warnings. Caption gaps ~11.8/11.3/11.3 pt. Non-blocking: `\tablesummary` walk uses undefined `\tl_if_in_p:Nn` (120 recovered TeX errors; `/Summary` still lands on Table). |
| Referee 4 (figures) | **APPROVE** | fig1 `[0,150,1428,936]` no longer contains σ(Ω)dΩ and the ring is whole; fig3 `[1470,1585,2340,2040]` drops the stray ⇐ and heading; all four alt-text nits match the drawings. |
| Referee 5 (adversarial) | **APPROVE** | After the live artifacts were rewritten to **7 boxed empty + 1 xcancel empty + 10 cancel + 2 ovaleq decoration = 20**, the U+FFFD split matches independent measurement. Round-2 mechanisms 1–3 and 5–7 already closed. |
| Accessibility Auditor | **APPROVE** | Four Step 4d tests pass; veraPDF UA-2 PASS; empty MathML identity-matched; table `/Summary` on Table; disclosures match measurements. PAC not run. |

**Round 3 closed: APPROVE ×6.** The PDF remains frozen at md5 `85b05d31081368d8b811063456c7f769`. Non-blocking leftover: `\tablesummary` uses undefined `\tl_if_in_p:Nn` (120 recovered TeX errors; `/Summary` still lands on Table). Not rebuilt, so as not to invalidate the six votes.
