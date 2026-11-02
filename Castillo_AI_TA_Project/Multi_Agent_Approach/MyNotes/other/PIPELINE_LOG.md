# Multi-Agent Pipeline — Run 5 Log

**Date:** 2026-07-30
**Spec:** `Multi_Agent_Outline.md`
**Batch:** 4 source PDFs, 24 pages, processed in parallel by per-document subagent chains.

Runs 1–2 (2026-07-06) and Run 3 (2026-07-23) covered the scattering lecture only. Run 4
(2026-07-29) was the first multi-input batch but stopped after Stage 1 — no assembled PDF and no
LaTeX output. Run 5 restarts the whole pipeline from a clean slate.

---

## Stage 0 — Ingest & Pre-flight Archive

Run-4 leftovers (`segments/`, `assembled/`, `Final_Product_Ready/`, `PIPELINE_LOG.md`) archived to
`Run_Archive/2026-07-30_094932/` before anything else ran; fresh directories created.

| Slug | Source PDF | Pages | Medium | Subject |
|------|-----------|-------|--------|---------|
| `scattering` | `Lecture-scattering-Hamiltonian_241022-forward.pdf` | 4 | handwritten | Scattering / Hamiltonian |
| `oscillations` | `Lecture-Oscillations-241119_241114.pdf` | 7 | handwritten (graph paper) | Small oscillations, normal modes |
| `rotations` | `Lecture-Rotations-Rigid-241031.pdf` | 12 | handwritten (graph paper) | Rotations, rigid-body dynamics |
| `comp1015` | `Lecture-241015_comp.pdf` | 1 | whiteboard photograph | Central potential, Kepler problem |

Handwritten documents rendered at 200 DPI. `comp1015` is a landscape board photo on a portrait
page; at 200 DPI its writing was too small to transcribe, so it was re-rendered at 600 DPI and
cropped to the board itself (4992×1937).

---

## Stage 1 — Segmentation

Reusable components: `tools/segment_notes.py`, `tools/check_coverage.py`, `tools/assemble_pdf.py`.
All subject-agnostic. Segmentation emits `segment_manifest.json` (exact crop rectangle per
segment) so downstream checks are numeric rather than visual.

**Four defects were found and fixed during the run, each by the review loop:**

1. **Printed ruling counted as ink.** Graph-paper grid lines are dark and span the full page, so
   every row looked occupied, no whitespace valley was ever found, and all three handwritten
   documents came out as exactly 5 *equal mechanical slices* per page. `suppress_ruling()` now
   drops any row or column inked across >55% of the page before profiling. Segment counts became
   content-driven (3–7 per page).
2. **The whiteboard is written in columns.** Horizontal strips across a 5-column board interleave
   unrelated derivations. Column panels are now segmented independently, top to bottom.
3. **Equal-slice fallback bisected figures.** When a page offered no whitespace valley,
   `split_tall` cut at evenly spaced positions, which land on content by definition. This was the
   dominant Stage 2 defect — it severed the `-z` axis label that fixes the sign convention in
   `oscillations`, the Euler-angle figure defining the α/β/γ convention in `rotations`, and the
   leading minus sign of the Binet equation in `comp1015`. Cuts are now placed only in blank gaps
   between ink bands, and an internally gapless block is kept whole rather than sliced.
4. **Symmetric column padding was over-constrained.** One shared boundary controlled both the
   right edge of a column and the left edge of its neighbour; on `comp1015` those two constraints
   became jointly unsatisfiable and a round-3 fix silently regressed a line round 2 had contained.
   Explicit per-column windows (`--col-windows`) decouple them.

**Final output: 104 segments.** Coverage verified numerically — every page retains ≥1.066× its
handwriting ink (excess = deliberate overlap). No page lost content.

| Slug | Pages | Segments | Stage 2 rounds |
|------|-------|----------|----------------|
| `scattering` | 4 | 19 | 1 |
| `oscillations` | 7 | 27 | 2 |
| `rotations` | 12 | 48 | 2 |
| `comp1015` | 1 (board) | 10 | 4 |

---

## Stage 2 — Expert Review Loop — CLOSED, all four documents 3/3 APPROVE

30 reviewer-agent runs across 9 panels. Reviewers verified crop geometry programmatically
(pixel-exact template matching, ink-mass accounting, connected-component containment scans)
rather than by eye, which is why the findings were actionable.

| Document | R1 | R2 | R3 | Rounds |
|---|---|---|---|---|
| `scattering` | APPROVE | APPROVE | APPROVE | 1 |
| `oscillations` | APPROVE | APPROVE | APPROVE | 2 |
| `rotations` | APPROVE | APPROVE | APPROVE | 2 |
| `comp1015` | APPROVE | APPROVE | APPROVE | 4 |

`comp1015` was the hardest input — landscape, five columns, glare, no clean gutters — and needed
four rounds. Its final containment scan (binarize, mask board frame and physical divider,
morphological closing, connected components at two granularities, test every bounding box against
all ten segment rectangles) reports **zero uncontained ink groups**.

Reviewer findings that changed the output are recorded in `segments/review_round1.md` and
`segments/review_round2.md`, and the transcription hazards were carried into every Stage 4b brief.

---

## Stage 3 — Assembly

| Document | Assembled PDF | Pages |
|---|---|---|
| `scattering` | `assembled/scattering_approved.pdf` | 20 |
| `oscillations` | `assembled/oscillations_approved.pdf` | 28 |
| `rotations` | `assembled/rotations_approved.pdf` | 49 |
| `comp1015` | `assembled/comp1015_approved.pdf` | 11 |

---

## Stage 4a — Reference Convention — CLOSED

**Goldstein, Poole & Safko, *Classical Mechanics*, 3rd ed.**, with **Fetter & Walecka Ch. 5
co-primary for `rotations`**. Two independent referees; verdicts ACCEPT WITH AMENDMENTS and
SURVIVES WITH AMENDMENTS. Full record in `Final_Product_Ready/SYMBOL_CONVENTIONS.md`.

The referees caught three things worth recording:

- **`rotations` follows Fetter & Walecka, not Goldstein Ch. 4–5** — stated in the lecturer's own
  hand ("Following Ch5 F&W (Skipping a lot)"). Its space/body axis convention is the *reverse* of
  Goldstein's, so importing Goldstein there would have inverted every equation in the segment.
- **The first draft of `goldsteinnotes.sty` was defective.** It bound `\reduced` to μ and `\lang`
  to ℓ batch-wide. Applied to `scattering` that silently rewrites the notes' **m** into **μ**;
  applied to `oscillations`/`rotations` it merges angular momentum with the *lengths* those
  lectures write as `l`. A macro that binds a quantity to a letter is a content edit disguised as
  notation. Both were removed; the style file now defines no such macro.
- **Ten cross-lecture symbol collisions** (μ/m, e/ε, φ/θ̃, α/φ, and `l`, `k`, `I`, `Ω`, `L`, `A`
  each carrying multiple meanings). The four documents are internally consistent and **mutually
  inconsistent by design**; no cross-lecture consistency pass may "fix" them.

Taylor was struck — there is no undergraduate-level passage in the batch.

---

## Stage 4b — LaTeX Transcription

| Document | `.tex` | Pages | Compile |
|---|---|---|---|
| `scattering` | `hc6001_2024-10-22_scattering_hamiltonian.tex` | 7 | clean |
| `oscillations` | `hc6001_2024-11-19_small_oscillations.tex` | 12 | clean |
| `rotations` | `hc6001_2024-10-31_rotations_rigid_body.tex` | 18 | clean |
| `comp1015` | *(in progress)* | — | — |

"Clean" = 0 errors, 0 warnings, 0 undefined references, 0 overfull **and** 0 underfull boxes,
verified by grepping the log rather than by eye.

**A correction made during this stage.** The `rotations` brief instructed that `zz − zz` on p. 5
be rendered as struck, derived from a reviewer's summary. The transcriber zoomed the manuscript,
found the strokes stop at the baseline of the line above — it is **not** struck — and reported the
departure rather than hiding it. The instruction was wrong and the strike was reverted. A strike
we invent is exactly as much a fidelity violation as a strike we drop.

---

## Stage 4c — Publication Review

*(pending)*
