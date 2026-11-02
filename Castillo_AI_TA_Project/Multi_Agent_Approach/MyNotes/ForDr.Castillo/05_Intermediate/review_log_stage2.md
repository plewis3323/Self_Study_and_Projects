# Stage 2 review log — scattering_hamiltonian

Three physics-PhD reviewers, working independently, on the segmented PNGs, the
figure crops and the alt text. Recorded round by round so the loop is auditable
(Success Criterion 3).

---

## Round 1 — verdicts: REVISE / REVISE / REVISE

**Submitted:** 17 segments (4/5/4/4), 150 px overlap, 5 figure crops, first
draft of `alt_text.json`.

**Principal findings**

| Reviewer | Finding | Severity |
|---|---|---|
| C | **The ink mask is wrong.** `(R<150) & ((B-R)<45)` discards blue pen and the red retraction mark — it sees 0.2 % of an 11k-pixel mark. The discriminator is GREEN: ruling is cyan (G−R ≈ +95), pen is violet (G−R ≈ +12). | blocker (tooling) |
| A | The page-1 seam at y917 cuts the beam/ring drawing; no clean cut exists anywhere in the 767–917 overlap band. | blocker |
| A | `page03_seg04` cuts the scattering-center diagram; `page04` seam separates the `−∂L/∂t` caret annotation from the equation it belongs to. | major |
| A, B, C | Figure crops slice words at the edges — `scat_fig3` reads "TTRACTIVE CASE"; `scat_fig2` clips the "R" of REPULSIVE and imports a foreign arrow. | blocker |
| A, C | **Colour-only information**: the page-1 trajectory is blue and the axis/cone lines black, separating by only ~2.5:1 in greyscale; the page-4 retraction is a red X. Neither named in words. | blocker |
| B | Alt text mis-states the ψ geometry: both ψ angles share one vertex and are measured **from the apsidal line**, not from the baseline. | major |
| B | Errata inventory needed downstream does not exist as a file. | major |
| B | Source errata confirmed: missing `/E` in the quadrature; missing minus on `du`; `f(x,y)` for `df`; missing `dt` on the `dH` line. `H = −(L − Σpq̇)` is **correct** and must not be flagged. | major |

**Changes applied:** ink mask rewritten on the green channel; segments re-cut
to 15 with overlap raised 150 → 250 px; four diagram bands declared
un-cuttable; all five crops re-cut against measured border-ink; alt text
rewritten to name the blue/black distinction and fix the ψ geometry;
`errata.json` created; `retracted_regions` added to the segment manifest.

---

## Round 2 — verdicts: REVISE / REVISE / REVISE

Brief stated what had changed and asked each reviewer to verify those changes
specifically and to hunt for regressions introduced by them.

**Principal findings**

| Reviewer | Finding | Severity |
|---|---|---|
| A, C | **The ink mask is still wrong for red.** The new rule gates on `max(RGB) < 235`; saturated red is (255,0,0), so it fails the darkness cap before the colour logic runs — 2.1 % of the mark seen, up from 0.2 %. | major (tooling) |
| A | fig1's bottom edge amputates 25 % of the emergent ring: the band runs to y1048, the crop ended at y843. | major |
| A | fig3 alt text calls the apsidal line "the outgoing asymptote", then calls it the apsidal line two sentences later. | major |
| A | `scat_fig0` is a Lanczos upsample, not a 600 dpi render; `render_dpi: 600` is false. | major |
| B | **A source error was silently corrected**: the source writes `sin⁻²(θ/2)`; the transcription set `sin²`. Policy applied to half a line and not the other half. | blocker |
| B | The `θ̃` convention is applied faithfully in markup but **never defined in the rendered document** — the declaration is a LaTeX comment. | blocker |
| B | A source display (the factored quadrature step with its two underbraces) was replaced by prose — and the erratum for that equation cites it as evidence. | moderate |
| C | Contrast tool invents a blue-pen layer in three figures containing none; `worst_layer` mis-assigned. | medium (tooling) |
| C | Manifest `ink_rows` not reproducible from the tool that wrote it (threshold mismatch). | low |
| A, C | **Both reviewers withdrew round-1 recommendations** after measuring: the wider fig1 and fig4 boxes score 3–7× worse on border ink, and the stray arrow beside fig3 cannot be excluded without slicing the heading. | — |

**Changes applied:** ink mask corrected to accept anything dark **or** strongly
coloured (11,405/11,405 red captured); content-bounds threshold raised after
the fix moved four seams via a scanner-edge artifact — final seams identical to
round 2; manifest made reproducible and the invocation recorded; fig1 extended
to y1070 so the ring is whole; fig0 re-rendered from the vector source at a
true 600 dpi; fig3 alt text corrected; `sin⁻²` transcribed as written and
flagged; the `θ̃` convention and every departure from the reference stated in
the document's own notation table; the factored display restored.

---

## Round 3 — verdicts: APPROVE / APPROVE / APPROVE

Submitted: the corrected build. Reviewers asked to confirm the round-2 fixes
and to approve only if the segments, crops and alt text are genuinely fit for
transcription.

**A, B, C all APPROVE.** Coverage is exact (the only uncovered ink row on
pages 1–3 is the last pixel row of the sheet), all four protected bands sit
inside a single segment, the ink mask captures 11,405/11,405 red pixels, and
the manifest is reproducible from `segment_run.json`. Residual nits at this
round were confined to one crop (fig1 bottom still imported the `σ(Ω)dΩ`
line; fig3 still imported a stray `⇐`) and to alt-text wording. Those were
not segmentation defects; they were taken by Referee 4 at Stage 4c and
re-cropped there (`[0,150,1428,936]` and `[1470,1585,2340,2040]`).

| Reviewer | Verdict | Residual handed downstream |
|---|---|---|
| A | APPROVE | NEW-11/NEW-12: fig1 still contains body text at the bottom of the crop; alt-text nits on the theta-arc and double-headed arrow. |
| B | APPROVE | One accessibility-layer string bug handed to Referee 3 (not a physics or errata defect). |
| C | APPROVE | Tooling-only: `check_coverage.py` still cannot fail (overlap inflates ink mass). |
