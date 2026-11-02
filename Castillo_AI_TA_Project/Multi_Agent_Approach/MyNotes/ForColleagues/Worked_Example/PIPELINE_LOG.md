# Pipeline Run Log — 2026-08-16

Second full run of the multi-agent pipeline on the same input as 2026-08-13,
undertaken to close the open items that run left behind. Nine reviewer agents
were used: 3 segmentation reviewers over 3 rounds, 5 publication referees over
3 rounds, and 1 Accessibility Auditor.

- **Input:** `Input/Lecture-scattering-Hamiltonian_241022-forward.pdf` (4 pages)
- **Slug:** `scattering_hamiltonian`
- **Output:** `Final_Product_Ready/hc6001_2024-10-22_scattering_hamiltonian.{tex,pdf}` (11 pages)
- **Previous run archived to:** `Run_Archive/2026-08-16_220625/`
- **Build audited:** MD5 `85b05d31081368d8b811063456c7f769` (supersedes `07b8e22921f1e63b0821db8e52c3f8a1`, which failed Stage 4c round 2)

---

## Result

| | 2026-08-13 | this build (`85b05d31`) |
|---|---|---|
| veraPDF PDF/UA-2 | PASS | **PASS** |
| Headings 1:1 with the outline | 16/16 | **16/16** |
| Text operators unreachable from the tag tree | 0 of 1909 | **0 of 3406** |
| Tagged content buried inside an `/Artifact` | not measured | **0** |
| Figure reading positions | 7/13/15/33/79 % | **6.7 / 15.9 / 17.8 / 33.0 / 69.3 %** |
| `TH` elements | **0** | **7**, all `/C /TH-col` |
| Table `/Summary` | **0** | **3 of 3, on the Table element** |
| PDF bookmarks | **none** | **16**, including "Remarks on Eq. (37)" and "Chapter 8. …" |
| Link annotations carrying `/Contents` | 0 | **all** |
| U+FFFD inside Formula elements | 45 | **20** — 7 in boxed empty shells, 1 in the `\xcancel` retraction, 10 in `\cancel` strokes, 2 in ovaleq decoration (Eq. 51). |
| Empty MathML with a spoken fallback on that same Formula | 0 | **8 of 8** (7 boxed + the `\xcancel` retraction). Ovaleq Eq. (51) is spoken but is **not** empty. |
| HTML companion heading levels | skipped h2 | **1/2/3/4, no skips** |
| HTML MathML / rasterised equations | 114 / 0 | **187 / 0** |
| Caption–`\toprule` gap | not measured | **11.0 / 10.5 / 8.3 pt** (all ≥ 6 pt) |
| Compile warnings about tag structure | not checked | **0** |

**Nine open items from the 2026-08-13 run are closed:** no `TH`; no bookmarks;
link annotations without `/Contents`; HTML skipping `h2`; `đ` announced as "d
with stroke"; no equation numbering or cross-references; the orbit angle
colliding with the scattering angle; `\cancel`/`\ovalbox` U+FFFD inside
formulas; and figure crops re-cut from the source page.

---

## Stage 0 — toolchain probe

Before anything else, a probe document containing one equation, one list, one
table and one figure was compiled and **inspected in the output** for
`/Formula`, `/L`, `/Table`, `/TH` and `/Alt`. All present. Two findings from
the probe shaped the run:

- **MathML needs at least three LuaLaTeX passes.** luamml writes the fragments
  on one pass and they are embedded on a later one; a two-pass build ships a
  document with `/Formula` elements and no mathematics attached.
- **`TH` is reachable** in this kernel through `table/header-rows`, which is
  what closed the previous run's largest structural gap.

## Stage 1–2 — segmentation, 3 rounds, 3 reviewers

Round 1: **REVISE ×3**. Round 2: **REVISE ×3** again, with most round-1
findings confirmed resolved and the remainder concentrated in the tooling
rather than the segments. Round 3: **APPROVE ×3**. Residual crop nits from
that round (fig1 importing the `σ(Ω)dΩ` line; fig3 importing a stray `⇐`)
were taken by Referee 4 at Stage 4c and re-cropped there.

| Round | Changes applied |
|---|---|
| 1 | Ink mask rewritten (below); segments re-cut 17 → 15 with overlap 150 → 250 px; four diagram bands declared un-cuttable; all five figure crops re-cut; alt text rewritten to name the blue/black distinction and correct the ψ-angle geometry |
| 2 | Ink mask corrected again for saturated red; content-bounds threshold raised; manifest made reproducible; figure 1 extended to contain the whole emergent ring; figure 0 re-rendered at a true 600 dpi; alt text corrected where it named the apsidal line as the outgoing asymptote |

**The ink mask was wrong twice, and both times it hid something.** The first
rule keyed on the blue channel and so discarded the blue pen *and* the red
retraction mark — it saw 0.2 % of an 11,405-pixel mark. The corrected rule
keys on green, which separates cyan ruling from violet pen, but still gated on
`max(RGB) < 235` and so still missed saturated red, seeing 2.1 %. The final
rule keeps anything dark **or** strongly coloured and captures **11,405 of
11,405**. Fixing it moved four seams — the exact regression a reviewer had
predicted — traced to a scanner-edge artifact stretching the content bounds,
and resolved by raising the bounds threshold. Final seams are identical to
round 2.

Final set: **15 segments** (3/4/4/4), 250 px overlap at every boundary, **8 of
11 seams on rows carrying zero ink**, **0 uncovered ink rows on any page**, and
all four protected bands whole inside a single segment.

## Stage 3 — assembly

`assembled/scattering_hamiltonian_approved.pdf`, 15 approved segments.

## Stage 4a — reference convention

Goldstein, Poole & Safko, *Classical Mechanics* 3rd ed., Ch. 3.10 and Ch. 8.
Every departure from it is now stated **in the document**, in the notation
table of Sec. 3, rather than only in a source comment a reader never sees.

## Stage 4b–4d — compilation and review

5 publication referees and 1 Accessibility Auditor. **All six returned REVISE
on the first pass.** Round 2 (md5 `07b8e229…`): Referees 2 and 3 APPROVE;
Referees 1, 4 and 5 REVISE; the auditor's session was rate-limited and never
voted. Round 3 (md5 `85b05d31…`) closed those blockers: **APPROVE ×5 referees
and APPROVE from the Accessibility Auditor.** The referees found no error in
the physics — one re-derived the entire chain independently and could not
break a step — and concentrated on fidelity, typesetting and honesty of the
artifacts.

Fixed in response:

- **A source display was replaced by prose.** The intermediate quadrature step,
  with its two underbraces, had been paraphrased away — and the erratum note
  for that very equation cited it as its evidence, pointing the reader at a
  line that was not in the document. Restored as a numbered display.
- **A source error was silently corrected.** The source writes
  $\sin^{-2}(\theta/2)$ in the denominator of the quotient rule; the
  transcription had set $\sin^{2}$. Reproduced as written and flagged.
- **Two "errata" were not errors.** A referee showed that
  $\cos(\tilde\theta'-\tilde\theta')=\cos 0=1$ is the correct *evaluation*, and
  that the omitted denominator in the first quotient-rule term is
  value-preserving. Both flags were withdrawn: a false erratum is as damaging
  as a missed one.
- **The tag tree was malformed.** The build emitted *"The structure Sect can
  not be closed"* twice and *"There are still open structures on the stack"* —
  while veraPDF passed. Isolated by bisection to `\sout` containing
  mathematics inside a theorem environment; fixed by striking mathematics with
  `\xcancel` and words with `\sout`. **0 warnings now.**
- **Two overfull boxes**, one of 68.5 pt where a table ran nearly an inch into
  the margin. Both gone.
- Table summaries, `/ActualText` on the boxed formulas, figure widths raised
  for legibility, every float now cited in the body, Gaussian units declared,
  the σ(Ω) ≡ σ(θ) identification stated, and the errata brackets unified into
  one device with a separate device for editorial additions.

---

## The tools were wrong more often than the document

Four defects in this run's own checkers were found by measuring against known
values or by a reviewer re-deriving the number independently. Each would have
produced a clean report on a defective document:

1. **Reachability resolved to the innermost marked-content frame.** Tagged
   content nested inside an `/Artifact` was counted as reachable. Corrected so
   an artifact anywhere in the enclosing stack wins.
2. **The MathML test read the wrong bytes and the wrong tokens.** It scanned
   concatenated page streams, where the MathML is not; and its emptiness test
   accepted `<mtext>` as content, so a shell containing only a replacement
   character passed. It reported `0 empty, 0 U+FFFD` while eight equations —
   including the headline result — carried no mathematics at all. Now reads the
   `/AF` embedded files and tests for real character content.
3. **The artifact word-scan could not see the text.** It looked for literal
   `(...)` strings; a tagged LuaLaTeX PDF shows text as hex CID strings, so the
   test could never fire whatever was artifacted. Now decodes both.
4. **The contrast tool reported the wrong ink at the wrong tone.** It admitted
   anti-aliased ruling as a "blue pen" layer in figures containing no blue pen,
   and measured each layer at its 2nd-percentile pixel — darker than the ink a
   reader sees. Now classifies on green and reports each layer's representative
   colour.

The transferable lesson from the 2026-08-13 run holds and is now double-attested:
**every serious defect was found by measuring the output, and several were
found only because a reviewer refused to accept a measurement it could not
reproduce.**

---

## Known-partial — stated plainly

1. **Eight equations export MathML with no content** (7 boxed results plus
   the `\xcancel` retraction). A box defeats the generator; `\xcancel` over
   mathematics produces an empty `/AF` as well. Each of those eight Formulas
   carries a curated spoken rendition as `/ActualText` on **that same**
   Formula element. Ovaleq Eq. (51) has a spoken rendition but is **not**
   empty — do not count it among the eight. Complete MathML for the boxed
   results is in the HTML companion.
2. **PAC 2026 was not run** — Windows-only, and this run was on Linux. It is
   the tool an OHIO reviewer will use and its verdict has not been obtained.
   veraPDF is the checker of record here. Acrobat was likewise unavailable, so
   the Acrobat rule map was walked by hand against equivalent measurements
   rather than by running Acrobat.
3. **PDF/UA-1 fails clause 7.7** for **178** formulas whose accessible
   representation is an associated MathML file — the UA-2 mechanism, which UA-1
   predates. Enabling the kernel's automatic Formula alt text would clear it
   and was **rejected**: it emits raw LaTeX source, which a screen reader reads
   aloud as markup. UA-1 also fails clause 6.1 (PDF 2.0 header) and clause 5
   (`pdfuaid:part=2`); both are inherent to declaring UA-2.
4. **`/Scope` is present**, via `/C /TH-col` on all 7 TH and ClassMap
   `/TH-col << /O /Table /Scope /Column >>`. An earlier draft of this log
   claimed it was missing; that was a false negative from looking for a
   direct `/Scope` key.
5. **Figures are source crops**, so labels inside them are images of text. The
   alt text describes the geometry rather than transcribing every glyph.
6. **Twenty U+FFFD in Formula `/AF` MathML**, split as **7 boxed empty + 1
   `\xcancel` empty + 10 `\cancel` strokes + 2 ovaleq decoration (Eq. 51)**.
   An earlier draft of this log said “8 boxed + 12 cancel”; that counted the
   retraction as boxed and put ovaleq’s two replacement characters into
   `\cancel`. Ovaleq is not empty and contains no `\cancel`. Not closed.
7. **`get_text()` of the retraction is fragmented** (`retract e d: L eq u a l s …`).
   The structure-tree `/ActualText` is present; content-stream extraction is
   messy. Disclosed rather than claimed as continuous prose.
8. **`check_coverage.py` still cannot fail** — overlap inflates ink mass.
   Tooling nit, not a publication blocker.
9. **`\tablesummary` expl3 walk is dirty in the log.** It uses undefined
   `\tl_if_in_p:Nn` (120 recovered TeX errors). `/Summary` still lands on
   all 3 Table elements. Not rebuilt after the six round-3 votes.

## Reviewer requests not actioned, and why

- **Redraw the figures as vector art** (two referees, as in the previous run).
  Declined: Operating Principle 8 requires every figure to be a crop of the
  source drawing and never a redrawing. The crop-quality complaints underneath
  the request were acted on instead.
- **Remove `[H]` and let figures float** (one referee, on layout grounds).
  Declined: float placement is exactly what appended all five figures to the
  end of the tag tree in the previous run, at reading positions 87–99 %.
  Pinning is what keeps them beside the text they illustrate.
- **Adopt Goldstein's capital Θ for the scattering angle.** Not adopted: the
  source writes θ throughout and the tilde already separates the two angles.
  The deviation is now recorded in the notation table.
