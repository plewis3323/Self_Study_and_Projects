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

   **Fixed in the style file on 2026-08-17, after this build.**
   `Final_Product_Ready/goldsteinnotes.sty` now uses `\tl_if_in:NnTF`, so
   **`Final_Product_Ready/goldsteinnotes.sty` is no longer the file that
   produced `85b05d31081368d8b811063456c7f769`** — it is one line different,
   and the audited PDF was deliberately not rebuilt so the round-3 votes
   still describe the artifact they were cast on. Compiling the unchanged
   `.tex` against the fixed style gives **0 recovered errors, lualatex exit
   0**, and a structure tree identical to the audited one: 1292 elements,
   16 H-elements, 0 unreachable operators, 3 Tables all carrying `/Summary`,
   7 `TH`, 187 Formula / 8 empty / 0 empty without a fallback. The next full
   run rebuilds against the fixed style and closes this item outright.
   Frozen copies keep the old line on purpose:
   `ForDr.Castillo/01_Deliverable/` and
   `ForColleagues/Worked_Example/Deliverable/` are shipped packages whose
   md5s are quoted in their own reports.

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

---

## 2026-08-20 rebuild — closing known-partial 9, and a six-round Stage 4c/4d cycle

The known-partial above predicted this outright: "the next full run rebuilds
against [the fixed style file] and closes this item outright." It did. First
compile against the corrected `goldsteinnotes.sty` (`\tl_if_in:NnTF`) gave
**0 recovered TeX errors** (was 120) and, after re-running
`tools/fix_pdf_mathml.py`, **`mathml_empty: 0`** again. That alone would have
been a one-round close. It was not: re-running the Stage 4c/4d review loop on
the rebuilt artifact, as Operating Principle 3 requires for any new run,
surfaced a further seven rounds' worth of defects the 08-16 approval had not
caught, because most of them were specific to text and layout the rebuild
itself did not touch — meaning they had shipped in the 08-16 PDF too, just
never looked at again once that round closed.

**Round 1** (md5 `0fcf4dde…`): 5 physics referees REVISE, auditor APPROVE.
The notation table (Table 3) had silently grown from the source's 2 rows to
6 with no disclosure; Fig. 1's alt text claimed a double-headed arrow linked
two blocks of text when only one is in the crop; Figs. 2 and 3 printed at
~163/186 dpi against the pipeline's own 300 dpi floor after an unrelated
resolution regression; a ~40% blank page-1 gap from `[H]` overflow.

**Round 2** (md5 `432b1699…`): REVISE again, same pattern. The round-1 fix's
new disclosure sentence for Table 3 had the Goldstein-vs-others attribution
**backwards** — independently verified against the source's own "NOTATION:
Goldstein / Others" comparison box, which the pipeline had apparently never
actually looked at directly in six prior review rounds across two builds.
Fixing page 1's blank gap had pushed the identical defect to page 2. Figs. 0
and 4 were found under the 300 dpi floor for the first time — never checked
before.

**Round 3** (md5 `ad53e3c5…`): REVISE. The *fix* to the Goldstein attribution
undercounted its own table by one row; the reworded ψ definition contradicted
how ψ is defined twice elsewhere in the same document (Figs. 2/3's own
captions); and the notation table itself — having grown to 8 rows across two
rounds of correction — no longer fit on its own page, reproducing the exact
`[H]`-overflow defect class a third time, now against the table rather than a
figure.

**Round 4** (md5 `14f07203…`): invalidated by a process failure, not a
document defect. The Prime Agent rebuilt the PDF mid-round to test one
referee's `\clearpage`-removal claim (found it false — removing the
`\clearpage` reproduces the stranded-heading defect it was added to fix, not
a clean page), reverted the source, but did not rebuild again before the
round's Accessibility Auditor finished — leaving the live PDF mismatched
from the frozen hash for part of the round. The auditor caught this by
re-checking its own md5 through the session and correctly REVISEd on process
grounds. Two genuine content defects were found regardless (a figure's
direction description, a caption's unsupported claim) and a stale manifest
number (185 vs. the correct 189, from a Formula count that had grown
mid-cycle). Going forward: no file under `Final_Product_Ready/` is touched
between launching a round and collecting all six verdicts.

**Round 5** (md5 `70b1381f…`): APPROVE ×4 + auditor, REVISE ×1 — on a figure
alt-text direction claim that itself had flipped between rounds 4 and 5
(two different reviewer instances reached opposite conclusions about which
way a line in Fig. 3 goes). Resolved by an independent Hough line-transform
analysis: 10+ concordant detections identified a single dominant line running
from the vertex down-and-right, and the round-4 "down-left" finding was
reconstructed as a manual-tracing artifact from an X-shaped stroke crossing
that fooled a nearest-cluster tracker.

**Round 6** (md5 `f6e5c207…`): **APPROVE ×6. Closed.** Two independent,
cross-validated methods (Hough clustering plus a quantitative
residual-based arrowhead-attribution test) settled the Fig. 3 dispute for
good, agreeing with round 5. A second minor figure defect (an "ellipse"
that is actually a pointed lens/vesica shape with visible cusps) was also
caught and fixed. The Accessibility Auditor's closing pass found one new,
narrow, non-blocking item — 5 Formulas (struck-through cancellation terms in
otherwise complete equations) carry a stray U+FFFD in their MathML, distinct
from and much smaller than the empty-MathML issue this same document shipped
with twice before.

**Assembling the Stage 5 hand-off package against the closed artifact
surfaced one more defect no prior round had checked**: the HTML companion's
`<img>` tags reference figures by bare filename, but the PNG files live in
`Final_Product_Ready/figures/`, not alongside `notes.html` — the images would
not resolve in a browser. This is a packaging gap, not a content or PDF
defect (no markup-validity check confirms a referenced asset actually exists
at that relative path), so it did not require reopening Stage 4c/4d; the
PNGs were copied alongside `notes.html` in both `Final_Product_Ready/html/`
and the hand-off package.

### The transferable lesson, now attested a third time

Every prior run's log has said some version of: measure the output, don't
trust a prior approval, don't trust the tool. This run adds a specific
corollary — **an approval closes a round, not a defect class.** The 08-16
run's APPROVE ×6 was real and was not re-litigated; but it also never
independently re-examined the notation table against the source's own
comparison box, never checked Figs. 0/4's resolution, and never opened the
HTML companion in anything but a markup validator. None of those gaps were
caused by the 2026-08-20 rebuild — the rebuild only gave a reason to look
again. A defect that survives one clean approval is not thereby verified; it
is simply a defect nobody has looked at recently.

### Closed this run

- `\tl_if_in_p:Nn` expl3 bug (120 recovered errors/compile) → `\tl_if_in:NnTF`, 0 errors.
- 8 empty-MathML Formulas → `fix_pdf_mathml.py`, identity-matched, `mathml_empty: 0`.
- Notation table: false Goldstein attribution (in both directions across two
  rounds), an unsupported "apsidal angle" term, an undercounted disclosure
  sentence, a geometrically inconsistent ψ row — all corrected and
  cross-verified against Goldstein's own text by two independent referees.
- Three separate instances of the `[H]`-overflow stranded-heading defect
  (Fig. 1/page 1, Figs. 2-3/page 2, the notation table/page 8).
- Two under-floor figure resolutions found and fixed (Figs. 2/3, then Figs. 0/4).
- Seven pixel-level figure alt-text inaccuracies, the most contested (Fig. 3's
  path direction) requiring three rounds and a cross-validated Hough-transform
  analysis to settle after two reviewer instances disagreed.
- A source transcription slip (`0<θ<π` for a source reading `0<θ≤π`).
- Stale reading-order/screen-reader walk files (twice), a stale MANIFEST
  number, a stale auditor report, an undisclosed-then-disclosed stale
  hand-off package.
- The HTML companion's broken image paths (found during Stage 5 packaging).
- A tool bug: `fix_pdf_mathml.py --in-place` never actually worked (missing
  `allow_overwriting_input=True` on the pikepdf open call).

### Still open, disclosed rather than closed

- PDF/UA-1 fails clause 7.7 on 189 of 198 Formulas — inherent to declaring
  UA-2; not a defect to fix, a consequence of the standard chosen.
- 5 Formulas carry a stray U+FFFD on an already-cancelled `\cancel`-stroke
  term (narrow, MathML-layer only, found in the closing round).
- PyMuPDF's `get_text()` reads `/ActualText`-bearing Formulas tripled/garbled
  (poppler is clean) — an extractor behaviour, not a structure-tree defect.
- Each HTML data table carries one leftover empty `<tr>` above its real
  header row.
- PAC 2026 confirmed installed and reachable on the attached Windows host
  but never run interactively — it has no CLI, and no operator session was
  available to any automated round.
- Two very minor documentation nits, judged non-blocking by the referees who
  found them: a hardcoded `(Figs. 2, 3)` cross-reference in the notation
  table (numerically correct, does not auto-update), and
  `Multi_Agent_Outline.md`'s `--sections` grep pattern undercounting on a
  document using the bracketed short-title `\subsection[...]{...}` form
  (currently self-cancelling with another factor in this build; worth fixing
  in the outline itself before a future run relies on the same coincidence).

---

## 2026-08-20, same day — PAC 2026 finally run for real, two tagging defects closed

The round-6 known-gaps list said flatly: "PAC 2026 confirmed installed and
reachable on the attached Windows host... but never run interactively — it
has no CLI, and no operator session was available to any automated round."
That changed a few hours later. The operator ran PAC 2026 (v26.1.0.0)
interactively against the frozen `ForColleagues/Worked_Example/` copy
(md5 `85b05d31...`) and, separately, a colleague ran Adobe Acrobat's
checker against the same file. Both reports were shared as a one-page PDF
summary and a set of screenshots of PAC's expanded per-checkpoint detail
view — the summary alone would not have been enough to act on; the detail
view was.

**What the reports actually said, checked before acting on any of it:**

- **189 "Alternative Descriptions" failed (PAC) / "Character encoding:
  Failed" (Acrobat)** — both re-confirmed limitations already disclosed in
  round 6: the clause-7.7 `/AF`-only Formula count (198 − 9 = 189, an exact
  match) and the toolchain's standing ToUnicode gap that
  `Multi_Agent_Outline.md` itself already names as "the rule this toolchain
  actually fails." Neither was new. Neither needed action.
- **7/7 `TH` cells failed "Table header cell has no associated data cells"
  (PAC).** Real, and traced to its exact cause rather than patched blind:
  every header cell carries `/Scope` only through `/C /TH-col` plus this
  document's own `/ClassMap` — a fully spec-conformant ISO 32000-2
  indirection, and the mechanism the outline deliberately chose specifically
  *because* a checker that only looks for a direct `/Scope` key false-negatives
  here. PAC, evidently, is exactly that checker (consistent with its own
  admission mid-check that it does not fully support PDF 2.0).
- **57/58 "Part" and 8/8 "Note" structure-element warnings (PAC).** Traced,
  not assumed: walking the PDF's own `/RoleMap` with pikepdf (not trusting
  PAC's characterization at all) showed `/text-unit → /Part` and
  `/float → /Note` are **latex-lab's own built-in default role table** for
  the `pdf2`/UA-2 namespace (`tagpdf-ns-latex-lab.def`) — every ordinary
  paragraph is auto-wrapped `text-unit` (57 of them), every figure/table
  LaTeX float environment is auto-wrapped `float` (5 figures + 3 tables = 8).
  Neither is something `goldsteinnotes.sty` or the transcription chose;
  both are upstream defaults of the experimental PDF-2.0 tagging support
  this pipeline already relies on for everything else.
- **8/10 "Caption" and 2/115 "P" warnings (PAC).** Not investigated this
  round — no root cause was traced, so nothing was fixed. Disclosed in
  `MANIFEST.json known_gaps` rather than guessed at.

**Fixed:** `tools/fix_pdf_tagging_defaults.py`, a new post-build patch script
in the same family as `fix_pdf_mathml.py` — additive/redirective only, no
content, MCID, or reading-order change. It remaps `/RoleMap /text-unit` to
`/P` (this document already role-maps plain `text → P`, so a paragraph
wrapper landing on the same standard tag is the natural fix, not an
invention) and `/float` to `/Div`, and adds a literal `/A` to each `TH`
duplicating what `/ClassMap /TH-col` already resolves to — redundant with
the existing `/C` reference, but readable by a checker that never resolves
`ClassMap` at all.

**Verified before shipping, not after:** veraPDF UA-2 stayed PASS and UA-1
failed the identical three clauses as before (5, 6.1, 7.7 — nothing added,
nothing removed); `tools/check_structure.py`'s full Step 4d numeric-test
suite passed clean, with `Part` and `Note` gone entirely from the
element-type counts (`P`: 115→173, `Div`: 12→20, matching the 58/8 counts
exactly) and `TH` still 7; the hand-off package's own `verify.sh` was re-run
against the patched, re-propagated package end to end and passed clean.

**md5 f6e5c207... → 0c4d468a...** Physics content is byte-for-byte
untouched — only `StructTreeRoot` metadata changed — so round 6's physics
`APPROVE ×6` stands and physics referees were not re-convened; this was a
Stage 4d-only patch. `ForColleagues/Worked_Example/` was deliberately left
on the old `85b05d31...` build per standing policy (frozen evidence), with
the divergence recorded in `ForColleagues/CHANGES_SINCE_RUN.md` instead.

### The lesson this adds

Round 6 already wrote "an approval closes a round, not a defect class."
This is a second instance of exactly that, on the same document, the same
day: six rounds of dedicated accessibility auditing never caught two real
tagging defects because no round ever had PAC's actual checkpoint-level
output — every prior "PAC not run" disclosure was accurate but incomplete
in a way nobody could see until an operator with a Windows session actually
ran it and looked past the summary page. The summary page (27 Passed / 1
Failed / 3 Needs-manual-check / 1 Skipped) would have looked like
confirmation of what was already known. The detail view is what had the
two real findings in it.

---

## 2026-08-20, same day, second addendum — declared standard switched UA-2 → UA-1; 189-formula gap closed

The operator pushed back on the previous addendum's framing: PAC 2026's own report header reads `Standard: PDF/UA-1`, not UA-2. If the goal is a PAC pass, UA-1 is what PAC actually checks — and this pipeline had been declaring UA-2 throughout, with the single largest failure bucket (189 of 198 Formulas, "Alternative Descriptions"/clause 7.7) explicitly disclosed as "inherent to the UA-2 `/AF` mechanism, which UA-1 predates." No tagging patch was ever going to close that gap while UA-2 stayed declared.

**Checked before acting, not assumed:** `pdfstandard=ua-1` turns out to be a real, first-class, kernel-supported target — `g__pdfmeta_standard_pdf/UA-1_prop` in `latex-lab`'s own `pdfmanagement.ltx`, not a workaround bolted on. Reading `latex-lab-math.ltx` directly (not guessing from behavior) found the exact mechanism: on UA-1 detection the kernel's own code prints `PDF/UA-1 detected. Enabling alt text on Formula` and flips `math/alt/use` true, which makes *every* Formula structure element receive a non-empty `/Alt`, where previously only Formulas with an explicit `\formulaalt` call (9 of 198) got one.

**Trialed in a scratch copy before touching the deliverable:** `\DocumentMetadata` changed from `pdfstandard=ua-2,pdfversion=2.0` to `pdfstandard=ua-1,pdfversion=1.7`. Three lualatex passes, 0 recovered errors. veraPDF UA-1 flipped **FAIL → PASS**. `check_structure.py`'s math test went from "9 carry a spoken fallback" to **"198 carry a spoken fallback."** The 9 hand-authored `\formulaalt` `/ActualText` entries were confirmed untouched and still present alongside the new `/Alt` (assistive tech prefers `ActualText` over `Alt` when both exist, so nothing regresses for those 9). No other Step 4d numeric test changed. Only after this passed clean was it applied to the real deliverable.

**Disclosed, not hidden:** inspecting the actual `/Alt` strings the kernel writes for the other 189 Formulas found they are the raw LaTeX source, wrapped in a fixed template — `"LaTeX formula starts \begin{equation}...\end{equation} LaTeX formula ends"`. That is real, non-empty alternative text that satisfies a presence-based conformance check (veraPDF, almost certainly PAC), but a screen reader announcing LaTeX markup syntax is not the same quality as the 9 hand-authored spoken renditions. This is recorded as open future work in `MANIFEST.json known_gaps`, not claimed as fully solved.

**A process mistake caught before shipping:** switching `pdfversion` requires a full source recompile, not a post-build patch — and a full recompile regenerates the PDF from scratch, silently dropping any *earlier* post-build patch that isn't reapplied. The intermediate rebuild (md5 `8cce35a0...`) had `mathml_empty` regress from 0 back to 8 because `tools/fix_pdf_mathml.py`'s splice (from the previous run) had not yet been re-run against the new compile — caught by re-running the full `check_structure.py` suite before shipping, not assumed clean from the earlier fix having "already happened." Corrected by reapplying `fix_pdf_mathml.py`; final md5 `b92b19d2...` passes every Step 4d test clean.

**Also updated:** `tools/verify.sh` (root, `ForDr.Castillo/`, `ForColleagues/tools/`) now states UA-1 as the primary conformance check and UA-2 as the contrast check, reversing the prior framing — but the *top-level* `ForColleagues/verify.sh`, which targets the deliberately-frozen `Worked_Example/` (still genuinely UA-2, md5 `85b05d31...`, untouched), was left exactly as it was, since changing its framing would have made it describe a file that does not match it.

### md5 chain this addendum

`f6e5c207...` (round-6 close, UA-2) → `0c4d468a...` (+tagging-defaults patch, still UA-2) → `8cce35a0...` (UA-1 recompile + tagging-defaults reapplied, but MathML splice not yet reapplied — never shipped) → `b92b19d2...` (+MathML splice reapplied — **current**). Physics content is identical across the entire chain; only `\DocumentMetadata`'s declared standard and `StructTreeRoot` metadata changed.

### The lesson this adds

A declared standard is a choice with real, checkable downstream consequences, not a label — UA-2 was chosen for good reasons earlier in this project (PDF 2.0's richer `/AF` math-tagging), but the institutional checker that will actually be quoted back to this document checks UA-1, and no amount of tagging cleanup inside a UA-2 declaration was ever going to satisfy a checker built around UA-1's stricter, older alt-text rule. Read the kernel's own source before assuming a behavior is a limitation — the "alt text on Formula" mechanism was sitting in `latex-lab-math.ltx` the whole time, gated behind a document-metadata switch this pipeline had simply never flipped.

---

## 2026-08-20, same day, third addendum — re-ran PAC against the fixed build; a tested-and-disproven hypothesis, and the actual result

The operator re-ran PAC 2026 against the fixed, UA-1 build and shared both the summary and, again, the full expanded checkpoint detail (157 screenshots this time, organized by role into `Formula/`, `P/`, `Table/`, `L/`, `Whitespace/` folders — considerably more usable than manually expanding categories in the GUI one at a time).

**The headline result is a real, large improvement.** PAC's overall verdict flipped from a red "This PDF file is not PDF/UA compliant" to a yellow "It's possible that some PDF/UA requirements aren't met" — and **every single Failed checkpoint dropped to zero**: Structure elements 7→0, Alternative Descriptions 189→0 (239/239 now pass — the same total item count as before, confirming this wasn't a different file or a narrower check). Both fixes from the earlier addenda worked exactly as intended.

**One number moved the wrong way and got a real investigation, not a guess.** Structure tree warnings rose 75→151, even though the Part/Note fix eliminated 65 of the original 75. Before writing any more `.tex`, the obvious hypothesis — that the 189 formulas now carrying the UA-1 switch's auto-generated raw-LaTeX-source `/Alt` were tripping a PAC content-quality heuristic — was tested against the actual screenshots rather than assumed. It failed the test: `Formula_007_page-2.png` and `Formula_008_page-2.png` flag Eq. (9) and Eq. (10) — `eq:sigma-general` and `eq:sigma-T-def` — two of the eight equations that already carry hand-authored, high-quality `\formulaalt` spoken renditions from the very first accessibility work on this document. PAC flagged them anyway. Direct measurement against the PDF's own structure tree found the real pattern instead: **exactly 52/52 display-class Formulas flagged, 0/146 inline-class Formulas flagged** — an exact match to the document's own display/inline split, with zero correlation to alt-text presence or quality. The same 100%-of-instances pattern held for Table (3/3) and List (2/2, both matching the document's total table/list count exactly), while `P` (94/172) only partially resolved to a known cause (58 are the same paragraphs the Part-remap moved the warning onto, not eliminated it; the rest — including the pre-existing 2 title-block warnings — remain only loosely characterized as "short single-sentence paragraphs," not confirmed).

**Conclusion, and why no further `.tex` edit follows from it:** a checkpoint that fires on literally every instance of a role regardless of content is not measuring a property of that content — it reads as PAC's Matterhorn implementation flagging every block-level Formula/Table/List for mandatory human confirmation, structurally the same category as the outline's own "three items no tool decides" (reading order, color contrast, table summary). Writing spoken-math alt text for the remaining 44 display formulas was budgeted and then not done, because the one hypothesis that would have justified it was tested first and failed. This is disclosed as a verdict, not chased as a defect: **0 Failed, 151 Warned, all 151 traced to blanket per-role advisories rather than per-instance defects** (P's residual ~34 unexplained instances the exception — genuinely open, not yet traced).

### The lesson this adds, again

The previous addendum's own closing line — "read the kernel's own source before assuming a behavior is a limitation" — cuts the other way here: read the *evidence* before assuming a hypothesis is right, even a well-reasoned one. The raw-LaTeX-alt-text theory was specific, plausible, and consistent with everything disclosed about that trade-off so far — and wrong. Checking it against two screenshots before touching the `.tex` again avoided writing 44 formula descriptions that the data already show would not have moved the number they were meant to fix.

---

## 2026-08-20, same day, fourth addendum — every remaining open item investigated to a stated conclusion

Told to keep going until every point raised was addressed, not just the ones already closed. Four items were still open at the end of the third addendum: Table/L's mechanism (asserted blanket, only sampled once each), Whitespace (not investigated at all), P's residual ~34 (characterized as "loosely," not confirmed), and Adobe's Character-encoding failure (cited as a known limitation, never re-tested against the current build). Each got a real check.

**Table and L: the blanket-advisory read now holds across varying complexity, not just one sample.** All 3 Table screenshots and both L screenshots were checked. A 2-column/5-row table, a 2-column/3-row table, and a 3-column/8-row table are all flagged identically; a 2-item list and a 4-item list are both flagged identically. Content size and complexity don't distinguish flagged from unflagged, because *nothing* is unflagged — 100% of both roles, same as Formula. This generalizes the earlier finding rather than just repeating it once more.

**Whitespace (6): root cause found, not just observed.** None of the 6 screenshots carry a location marker, but all 6 land on pages 5, 5, 8, 8, 9, 9 — the document's three table pages, two each. That is the `\noalign{\tablesummary{...}}` row `goldsteinnotes.sty` inserts to attach `/Summary` to the `Table` element rather than the first `TH` — the exact mechanism already known to leave a leftover empty `<tr>` in the HTML companion. This is its PDF-side twin: a whitespace-only tagged span PAC can't localize, once per table.

**P (94/172): pushed from "loosely characterized" to substantially explained.** Six of the ninety-four have no page number at all (blank screenshots, `page-none` in the filename) and fall in the file sequence immediately around pages 5, 8, and 9 — the same 2-per-table pattern as Whitespace, almost certainly the identical six document locations counted twice by two different PAC checkpoints, not twelve separate defects. At least 58 more are the Part→P relocation already known from the second addendum. Seven direct samples of the remainder (not one, not two) all turned out to be short lead-in or transition clauses immediately beside a display equation — "gives" (one word), "Eq. (18) then becomes," "Substituting into Eq. (9) gives," "22 October 2024," and three longer but still equation-adjacent lead sentences. That's a real, consistent, checked pattern: this document's prose style gives nearly every one of its 52 display equations its own short introductory clause as a separate paragraph. Not a defect — these are legitimate sentences — and not fixed, because closing it means merging dozens of clauses into their equations throughout content that already passed 6 rounds of physics review, for a Warned-tier, not Failed-tier, finding.

**Character encoding: re-tested, not re-cited.** Adobe's one Failed item was reported against the frozen `85b05d31...` build and had only ever been *cited* as `Multi_Agent_Outline.md`'s known limitation, never actually re-checked against the current file. Extracted all text from the current `b92b19d2...` build with two independent extractors (PyMuPDF, poppler's `pdftotext -enc UTF-8`) and scanned for U+FFFD and Private-Use-Area codepoints — the signature of a ToUnicode gap. Zero found by either, across 14,966 characters; every font carries a `/ToUnicode` CMap, confirmed directly via pikepdf. This isn't proof Adobe's own checker would pass — its method may be stricter than a text-extraction scan — but it's real evidence against the finding still applying to this build, and the honest next step (re-run Adobe against `b92b19d2...` specifically) is stated rather than assumed away.

**Where this leaves the document:** every item raised across all four addenda today now has either a fix (TH scope, RoleMap, UA-1 switch — closing 196 Failed checkpoints to 0) or a stated, evidence-based conclusion for why no further change follows (Formula/Table/L's blanket advisory, Whitespace/P's `\noalign` twin, P's equation-lead-in prose pattern, Character encoding's untested-on-this-build status). Nothing remaining is an open question answered with a guess.

---

## 2026-08-20, same day, fifth addendum — told to keep trying, not stop at "not worth it"; found a real, previously-undetected defect

Told explicitly that the point of sharing PAC's errors was investigate → fix → verify, not investigate → disclose → stop. Two of the "blanket advisory, not fixable" conclusions from the fourth addendum were re-opened rather than left there.

**Table (3/3 flagged): re-investigated past "no attribute at all," and it was wrong.** The fourth addendum checked Table elements for a `/C` class and found none, concluded there was nothing analogous to the TH-scope fix to try, and moved on. That check stopped one level too shallow: it looked for `/C`, not for whether the `/Summary` this document *does* attach to every Table is actually valid PDF. It is not. `/Summary` was landing as a **bare top-level key on the `Table` `StructElem` dict** — not a key ISO 32000 defines anywhere on a structure element. The spec's table attributes (`/RowSpan`, `/ColSpan`, `/Headers`, `/Scope`, `/Summary`) live inside `/A` with `/O /Table`, the exact same location `/Scope` needed for `TH` in the very first fix today. `goldsteinnotes.sty`'s own comment even says so in hindsight: "this kernel offers no documented key for it — so it is written onto the Table structure directly." `check_structure.py`'s own test has checked for the string "/Summary" anywhere on the element since this document's second accessibility round in August — never for where. Confirmed by inspecting all three tables directly with pikepdf: `{'/ID', '/K', '/P', '/S', '/Summary', '/Type'}` — no `/A` at all. This plausibly explains 100% of Tables being flagged "possibly inappropriate use" all along; a UA-1 reader that only looks at `/A` sees a Table with no summary whatsoever.

**List (2/2 flagged): had exactly the pattern the TH fix already solved once.** Unlike Table, `L` elements do carry `/C /enumerate`, resolving via `/ClassMap` to `<</O /List /ListNumbering /Ordered>>` — the identical ClassMap-only-attribute shape as `TH`'s `/Scope`. Fixed the same way: a literal `/A` duplicating the resolved dict.

**Fixed, verified, and — critically — proved the verification itself works, not just the fix:** extended `tools/fix_pdf_tagging_defaults.py` with `fix_table_summary_attr()` (promotes the existing `/Summary` text into a proper `/A`, additive alongside the legacy key) and `fix_list_numbering()` (mirrors `fix_th_scope()` for `L`). Before trusting `check_structure.py`'s existing table-summary test to confirm the fix, it was checked and found **unable to catch this defect at all** — its regex matched "/Summary" wherever it appeared, so it would report "pass" whether the key was spec-valid or not. Extended it with a new field, `tables_summary_not_in_A`, that resolves the `/A` reference (indirect or inline) and confirms `/O /Table` and `/Summary` are actually inside it. **Ran this new test against the OLD build before trusting it against the new one**: it correctly failed, listing all three table xrefs, against a build known to have the bare-key-only version — the same discipline as every other fix today, prove the test can fail before trusting it to pass.

**md5 `b92b19d2...` → `bf4452a1...`.** veraPDF UA-1 stayed PASS, all Step 4d numeric tests stayed clean, `tables_summary_not_in_A` now empty. Not yet re-verified against a live PAC run (that would require the operator running PAC again, which has not happened since this fix) — so the *hypothesis* that this closes the Table/List warnings is well-founded (spec-invalid attribute, same class of gap as the already-confirmed-effective TH fix) but not yet *confirmed* by PAC the way the TH and RoleMap fixes were. Stated as such, not oversold.

**Formula (52/52) reconsidered and left alone, on purpose, not by default.** Formula elements' `/C /display`/`/inline` also resolve only through `/ClassMap`, the same shape as the three defects just fixed. Checked before deciding not to act: `/inline` uses the identical mechanism and is 0% flagged, so an unresolved-ClassMap theory is directly contradicted by the data that would need to support it, unlike Table and List where 100% of the *only* instances that exist are all flagged. Not fixed because the evidence says it would not help, not because it was not considered.

### The lesson this adds

"Checked for an attribute and found none" is a different finding from "checked whether the attribute that exists is valid," and the fourth addendum's Table conclusion — no `/C`, therefore nothing to fix — quietly conflated the two. The same discipline that caught the raw-LaTeX-alt-text hypothesis being wrong (test before writing more `.tex`) also applies to *not* giving up: a "blanket advisory" conclusion is itself a hypothesis, and this one had an actual attribute-placement bug sitting underneath it that a slightly deeper look found. The verification tooling itself is not exempt from this — `check_structure.py` had carried a real blind spot in exactly the area it was supposed to guard since this document's second accessibility round, and the fix for the document was not trusted until the fix for the *test* was proven able to fail first.
