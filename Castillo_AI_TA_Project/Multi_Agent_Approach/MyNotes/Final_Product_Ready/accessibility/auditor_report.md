# Accessibility audit — HC 6001, Scattering by a Central Potential; the Hamiltonian

**Auditor:** Accessibility Auditor, round 6 (independent vote). Stage 4c/4d closed this round: APPROVE from all 5 physics referees and this auditor.
**Document:** `Final_Product_Ready/hc6001_2024-10-22_scattering_hamiltonian.pdf`
**Build audited:** MD5 `f6e5c207ecb322c6c53eaca39ba6ee64`, 11 pages. Confirmed at session start, mid-session, and immediately before this verdict — unchanged throughout, and the freeze held for the entire round (see `review_log_stage4c.md`'s round-4 entry for the process failure this discipline was adopted in response to).
**Standard:** WCAG 2.1 Level AA as adopted by Ohio University; PDF/UA-2 (ISO 14289-2).
**Checkers run this round:** `tools/check_structure.py`, `tools/check_contrast.py`, veraPDF 1.30.2 `-f ua2` and `-f ua1`, plus independent object/tag/HTML/geometry walks via `pikepdf`/PyMuPDF. PAC 2026 confirmed installed and reachable on the attached Windows host but not run (no interactive session available to this agent). Acrobat not available.

This report does not reuse PIPELINE_LOG, MANIFEST, or any prior `auditor_report.md` as evidence — every number below was independently measured on this exact file this round. This document's notation table, pagination, and figure alt text each went through multiple rounds of correction (see `review_log_stage4c.md` for the full six-round history); this report describes only the final, approved state.

---

## What is still wrong

Stated first, because a reader who finds an unlisted defect will rightly discount everything else here.

1. **5 Formulas carry a stray U+FFFD on an already-cancelled `\cancel`-stroke term.** Eqs. 25, 36, 48, 50, 53 — each a complete, correct display equation with one algebraically-cancelled term struck through. This is distinct from, and much narrower than, the empty-MathML issue that shipped in earlier builds of this document: `mathml_empty: 0` (verified, see §6) — these 5 Formulas are *not* empty, they simply carry one stray replacement character inside otherwise complete MathML, on the struck term specifically. Confined to the MathML semantic layer: 0 replacement characters in the primary content-stream text via both PyMuPDF and pdftotext. Disclosed, not treated as blocking.
2. **PDF/UA-1 fails 3 rules / 191 checks.** Clause 6.1 (`%PDF-2.0` header) and clause 5 (`pdfuaid:part` = 2) are artefacts of declaring UA-2. Clause 7.7 is **189** checks: 198 total Formula elements − 9 that carry `/ActualText` (the boxed/xcancel results plus ovaleq Eq. 51) = 189 lacking the element-level fallback UA-1 requires and UA-2's `/AF` MathML mechanism supersedes.
3. **PAC 2026 was not run.** Confirmed installed and reachable on the attached Windows host (`Get-StartApps` finds `PAC.exe`) but it has no CLI/batch mode and requires an interactive operator this automated audit round did not have. veraPDF 1.30.2 is the checker of record here and is not a substitute for it.
4. **Figures are source crops**, so labels drawn inside them are images of text. Alt text describes the geometry and names the labelled quantities but does not transcribe every glyph.
5. **`get_text()` of several `/ActualText`-bearing Formulas reads tripled/garbled under PyMuPDF** (poppler/`pdftotext` is clean on the same passages). Root cause: PyMuPDF applies the parent Formula's single `/ActualText` independently to each of that Formula's underlying marked-content spans rather than de-duplicating by structure element. The struct tree itself carries exactly one `/ActualText` per Formula — an extractor behaviour, not a PDF-authoring defect.
6. **Two minor, non-blocking documentation items**, judged by the referees who found them not to warrant a rebuild: the notation table's ψ row cites "(Figs. 2, 3)" as a hardcoded cross-reference rather than `\ref{}` (numerically correct as shipped, does not auto-update); and `Multi_Agent_Outline.md`'s Command Reference `--sections` grep pattern undercounts on a document using the bracketed short-title `\subsection[...]{...}` form — the undercount happens to be offset by another factor in this build, giving the right number for compensating reasons. The second item is a note for the pipeline's own documentation, not a defect in this deliverable.

`/Scope` is **present**: all 7 TH carry `/C /TH-col`, and the document's ClassMap resolves `/TH-col` to `/O /Table /Scope /Column`. `/Summary` sits on the three Table elements, not on any TH.

Caption–`\toprule` gaps, measured at 300 dpi from caption-text bottom to the first rule below it: **≈13.7 / 13.4 / 11.3 pt** across the three tables. All clear the 6 pt floor.

---

## 1. The four Step 4d numeric tests

Measured by `python3 tools/check_structure.py … --alt segments/scattering_hamiltonian/alt_text.json --sections 16`.

| # | Test | Result | Acceptance | Verdict |
|---|---|---|---|---|
| 1 | Heading inventory | **16** H-elements (H1 4, H2 10, H3 2) against **16** sectioning commands, 0 skipped levels | 1:1 with the outline | **PASS** |
| 2 | Content reachability (MCID walk) | **0 unreachable** of **3505** text operators; 23 decoration, 3482 reachable | zero unreachable | **PASS** |
| 3 | Artifact audit | **134** artifact frames, unclassified; **0** carry words; **0** bury tagged content | nothing meaningful is an artifact | **PASS** |
| 4 | Figure reading position | 5 figures at **6.5 / 15.4 / 17.2 / 31.9 / 67.0 %** | none clustered at the end | **PASS** |

Outline bookmarks: **16**, independently re-verified across three separate rounds (4, 5, 6) that every destination points to the page actually containing its heading's own text — no off-by-one drift anywhere in the outline.

## 2. Machine check

- **veraPDF 1.30.2, `-f ua2`:** PASS. `isCompliant="true"`, 0 failed checks. Matches this folder's `verapdf_ua2.xml`/`.txt`.
- **`-f ua1`:** FAIL, 3 rules / 191 checks total — analysed in item 2 above. Matches this folder's `verapdf_ua1.xml`/`.txt`.
- **PAC / Acrobat:** not run (see item 3 above).

## 3. The MDAS five

| # | Check | Evidence | |
|---|---|---|---|
| 1 | Permission flag set | not encrypted; accessibility permission bit set; no extraction restriction | PASS |
| 2 | Title present | `/Title` "Scattering by a Central Potential; the Hamiltonian"; `/DisplayDocTitle true` | PASS |
| 3 | Full text, not image-only | **16,724** characters extracted across 11 pages, 0 replacement characters | PASS |
| 4 | Language specified | catalog `/Lang (en-US)` | PASS |
| 5 | Alt text on every figure | **5/5**, each matching `alt_text.json` byte-for-byte, none equal to its caption | PASS |

## 4. The 7 Core Skills

| OHIO Core Skill | Verdict | Evidence |
|---|---|---|
| Headings for clarity and logical structure | **Satisfied** | 16 H-elements 1:1 with the outline, 0 skipped levels, 16 correctly-targeted bookmarks |
| Meaningful alt text for images | **Satisfied** | 5/5 specific and drawing-accurate, distinct from captions; fig1 names the blue path vs black axis in words (WCAG 1.4.1); each went through 3-6 rounds of independent pixel verification |
| Sufficient colour contrast | **Satisfied** | body **21:1**; figure blue pen **8.45:1**. Lowest *content* ratio 8.45:1 against a 3:1 non-text floor |
| Format lists correctly | **Satisfied** | L 2, LI 6, Lbl 16, LBody 6; every LI has Lbl and LBody |
| Create descriptive links | **Satisfied** | 36/36 link annotations carry `/Contents`; no "click here", no bare URLs |
| Design accessible tables | **Satisfied** | 3 data tables, 7 TH with `/C /TH-col`, caption and `/Summary` on each Table element |
| Captions and transcripts for A/V | **Not applicable** | no time-based media |

## 5. The three items no tool decides

**Logical reading order — pass.** Figures sit at 6.5–67.0% of the tag tree, adjacent to the text/heading they illustrate, not dumped at the end. Independently re-walked across rounds 3-6 after every page-layout-affecting change (the `\clearpage` before the notation table, the figure display-width changes for pagination); each re-walk confirmed no orphaning or reordering.

**Colour contrast — pass, with the excluded layer disclosed.** PDF body text is rgb(0,0,0) at **21.00:1**. Figure crops: four are black pen at 21.00:1; `scat_fig1_beam_ring.png`'s worst content layer is blue pen at **8.45:1**. Printed ruling at 3.91:1 is excluded from the verdict as paper, not content. Greyscale blue/black separation in fig1 is 2.49:1, so the distinction is named in the alt text (WCAG 1.4.1).

**Table summary — pass.** `/Summary` sits on all 3 Table elements (verified by direct object inspection, not inferred), never on a TH. Summaries describe: orbit type by energy sign; classical vs quantum total cross section; and this document's symbols vs Goldstein, Poole & Safko. Caption–`\toprule` gaps all clear 6 pt.

## 6. Math

198 `Formula` elements; 153 distinct MathML files attached through `/AF`. **`mathml_empty: 0`** — the 8-Formula empty-shell issue present in earlier builds of this document is fully closed (`tools/fix_pdf_mathml.py`, identity-matched by equation number).

9 Formulas carry `/ActualText` (the 8 previously-empty ones, now non-empty but still carrying a spoken fallback, plus ovaleq Eq. 51). The 5-Formula `\cancel`-stroke U+FFFD issue is disclosed above (item 1).

## 7. HTML companion

Held to the same WCAG 2.1 AA bar. Measured on `Final_Product_Ready/html/notes.html`:

- **198** `<math` elements, exactly matching the PDF's 198 Formula elements; **0** rasterised equations.
- Heading levels **1 / 2 / 3 / 4** with no skipped levels.
- **5/5** `<img>` with alt from the sidecar, verified present in the compiled output byte-for-byte.
- **3** data tables, each with `<caption>` and real `<th scope='col'>` (7 header cells total).
- **Known non-blocking issue:** each of the 3 data tables carries one leftover empty `<tr>` above its real header row, left over from the `\noalign` `/Summary`-parking mechanism. Cosmetic; header promotion itself is correct.
- **Packaging fix applied this round:** the companion's `<img>` tags reference figures by bare filename (e.g. `src='scat_fig1_beam_ring.png'`); the PNGs are now copied alongside `notes.html` in both `Final_Product_Ready/html/` and this hand-off package's `01_Deliverable/html/`, so the images actually resolve when the file is opened in a browser. This had not been previously verified by any prior round's review, since markup validity checks do not confirm the referenced asset exists at that relative path.

---

## Verdict

**VERDICT: APPROVE**

This is the sixth and closing round of Stage 4c/4d review on this rebuild cycle. Every mandatory numeric test passes on independently re-measured numbers, not on a prior report. veraPDF UA-2 passes. Table `/Summary` is on Table, `/Scope` is in the ClassMap, MathML is non-empty for all 198 Formulas, caption–rule gaps all clear 6 pt, contrast clears with the ruling exclusion stated, and the HTML companion matches the PDF on MathML count and heading integrity — with its image-asset packaging corrected this round. The residual list above (item 1, the narrow `\cancel`-stroke U+FFFD; PAC unrun; the two documentation nits) is what I would put in front of an OHIO reviewer, and I would sign this file with those limitations disclosed.

---

## Addendum, same day (2026-08-20 14:xx) — PAC 2026 actually run; two tagging defects closed

"PAC unrun" above stopped being true a few hours after this report closed. The operator ran PAC 2026 (v26.1.0.0) interactively against `ForColleagues/Worked_Example/`'s frozen copy (md5 `85b05d31...`) and obtained its detailed per-checkpoint view, not just the summary this pipeline had previously had to disclose blind. A colleague separately ran Adobe Acrobat's checker against the same file. Full findings, root causes, and the fix are in `MANIFEST.json`'s `accessibility.pac_2026_review` and `PIPELINE_LOG.md`'s "same day" entry; summarized here for anyone reading only this report:

- **189 "Alternative Descriptions" (PAC) / "Character encoding" (Acrobat)** — both re-confirm limitations already disclosed above (item 1's clause-7.7 count, and this toolchain's standing ToUnicode gap). Verified, not new, no action.
- **7/7 `TH` cells, "no associated data cells" (PAC)** — real. `/Scope` reached them only through `/C /TH-col` + `/ClassMap`, which this report's §5 correctly states is conformant PDF, but which PAC does not appear to resolve (its own dialog admits incomplete PDF 2.0 support). **Fixed:** a literal `/A` now duplicates the resolved dict directly on each `TH`.
- **57/58 "Part" + 8/8 "Note" warnings (PAC)** — real, but not this document's defect: independently confirmed via pikepdf that `RoleMap /text-unit → /Part` and `/float → /Note` are `latex-lab`'s own built-in defaults for the `pdf2` namespace, applied to every paragraph and every figure/table wrapper respectively. **Fixed:** remapped to `/P` and `/Div`.
- **8/10 "Caption" + 2/115 "P" warnings (PAC)** — not investigated. Disclosed, not fixed.

Fix tool: `tools/fix_pdf_tagging_defaults.py`. Verified before shipping: veraPDF UA-2 stayed PASS, UA-1 failed the identical three clauses (5, 6.1, 7.7) before and after, and every Step 4d numeric test in §4 above still passes against the patched file (re-run, not assumed) — `Part`/`Note` are now absent from the element-type inventory entirely. Physics content is untouched; this was a Stage 4d-only, metadata-level patch, so the physics `APPROVE ×6` this report is part of stands unchanged.

**md5 `f6e5c207...` → `0c4d468a...`.** This report's own measurements above (§4–7) were taken against `f6e5c207...` and remain accurate for that build's physics content and everything except `/RoleMap` and `TH` `/A` presence; treat those two structural details as superseded by this addendum, not the rest of the report.

---

## Addendum 2, same day — declared standard switched UA-2 → UA-1; the 189-formula gap this report's §6 disclosed is now closed

The operator correctly pointed out that PAC 2026's own report header reads `Standard: PDF/UA-1` — PAC checks against UA-1, and this document had declared UA-2 throughout every round above. §6's "closed, not just disclosed" language about MathML referred to the empty-shell issue (8 Formulas), not this: 189 of 198 Formulas had no `/Alt` or `/ActualText` at all, because UA-2's `/AF`-only math tagging is exactly what UA-1's clause 7.7 does not recognize. No amount of tagging cleanup inside a UA-2 declaration could have closed that.

`pdfstandard=ua-1` (with `pdfversion=1.7`, since UA-1 caps at PDF 1.7) is a real, kernel-supported target in `latex-lab`'s own `pdfmanagement.ltx`, verified by reading the source rather than assumed: on UA-1 detection the kernel auto-writes `/Alt` on every Formula element. Trialed in a scratch copy first — 3 clean lualatex passes, 0 recovered errors, veraPDF UA-1 **FAIL → PASS**, all 198 Formulas now carry alt text (was 9) — then applied to the real deliverable.

**Disclosed, matching this report's own standard of practice:** the auto-generated `/Alt` for the 189 previously-bare Formulas is the raw LaTeX source (e.g. `s = \frac{\ell}{\sqrt{2mE}}`), not spoken math. It satisfies presence-based conformance (veraPDF, almost certainly PAC) but is lower quality than the 9 hand-authored `\formulaalt` spoken renditions, which remain untouched and take priority for assistive tech. Extending `\formulaalt` to more/all 198 is open future work, not done this round.

A recompile (required for the `pdfversion` change) regenerates the PDF from scratch and silently drops any earlier post-build patch not reapplied — caught before shipping by re-running the full Step 4d suite rather than assuming the prior fix persisted: an intermediate build briefly regressed `mathml_empty` from 0 back to 8 because `fix_pdf_mathml.py`'s splice had not yet been reapplied. Corrected before this addendum's final md5.

**md5 `0c4d468a...` → `b92b19d2...`** (via an intermediate `8cce35a0...`, never shipped). veraPDF UA-1 now PASS (was FAIL); UA-2 now FAIL on `pdfversion` alone (expected, no longer the declared standard, run for contrast per `Multi_Agent_Outline.md` Step 4d). Every other measurement in this report (§1–5, §7, the verdict itself) is unaffected — physics content and every other structural fact are unchanged across the whole chain.

---

## Addendum 3, same day — PAC re-run against the fixed build; verified, not assumed

The operator re-ran PAC 2026 against `b92b19d2...` and shared both the summary and 157 detail screenshots. **Confirmed: 0 Failed everywhere** (Structure elements 7→0, Alternative Descriptions 189→0 of 239 total items — same population as Addendum 1/2, fully closed). PAC's overall verdict moved from red "not compliant" to yellow "possible some requirements not met."

One number moved the wrong way — Structure tree Warned rose 75→151 despite the Part/Note fix removing 65 of the original 75 — and got tested, not assumed. The obvious hypothesis (the UA-1 switch's raw-LaTeX-source `/Alt` on 189 formulas tripping a PAC content-quality check) was checked against two screenshots before writing any more `.tex` and **failed**: `Formula_007`/`Formula_008` flag Eq. (9)/(10) — `eq:sigma-general`/`eq:sigma-T-def` — two of the eight equations with the best alt text in the document (hand-authored `\formulaalt` from the very first accessibility round). Measured against the PDF's own structure tree instead: 52 `/display`-class Formulas exist, 146 `/inline`; PAC flags exactly 52/52 display, 0/146 inline, with zero correlation to alt-text quality. Table (3/3) and List (2/2) show the identical 100%-of-population pattern. This reads as a blanket per-role advisory PAC applies to every block-level Formula/Table/List — structurally the same category as this report's own §5 ("the three items no tool decides"), not a fixable per-instance defect. **No further `.tex` edit follows**, and none was made: writing spoken-math alt text for the remaining 44 display formulas was considered and specifically not done, because the hypothesis that would have justified it was tested first and disproven. `P` (94/172) is only partially explained (≥58 are the Part-remap's relocated warning, ~34 open) and left disclosed rather than guessed at further. Full transcription: `pac_2026_detailed_report_2026-08-20.md`'s "Run 2" section.

---

## Addendum 4, same day — closing out every remaining item

The `P` residual and the Table/L/Whitespace findings were left as "not root-caused beyond the blanket pattern" above. Each was investigated to a stated conclusion rather than left there.

**Table/L**: all 3 Table screenshots and both L screenshots checked individually (a 2×5, a 2×3, and a 3×8 table; a 2-item and a 4-item list) — flagged regardless of size or complexity, confirming 100%-of-population blanket advisory rather than a one-sample coincidence.

**Whitespace (6)**: all 6 land on pages 5, 5, 8, 8, 9, 9 — this document's 3 table pages, 2 each — matching `goldsteinnotes.sty`'s `\noalign{\tablesummary{...}}` row (parks `/Summary` on the `Table` element) exactly, the same mechanism already known to leave an empty `<tr>` in the HTML companion. Root cause confirmed; not fixed (Warned-tier, would touch markup in all 3 already-approved tables).

**`P`'s residual**: 6 of the 94 turn out to be blank, page-less screenshots sitting in the same page-5/8/9 pattern as Whitespace — almost certainly the same 6 locations, double-counted by a second PAC checkpoint. ≥58 are the Part-remap relocation. The rest, sampled 7 times (not 1–2), are consistently short lead-in/transition clauses beside a display equation ("gives," "Eq. (18) then becomes," "Substituting into Eq. (9) gives," and four longer but still equation-adjacent examples) — a real, checked prose pattern this document shares with nearly every equation-heavy physics text, not a defect, and not one this round rewrites given the review cost against a Warned-tier finding.

**Character encoding** (Adobe's one remaining Failed item, never previously re-tested against this build): extracted all text from `b92b19d2...` with two independent extractors and scanned for the ToUnicode-gap signature (U+FFFD, Private Use Area). Zero found by either, across every font in the document. Not proof Adobe's own checker would now pass, but real evidence against the finding reproducing here — stated as a recommendation to re-test, not assumed either way.

Every item raised in this document's PAC-driven review today now carries either a fix or a stated, evidence-based reason none follows. Full evidence: `pac_2026_detailed_report_2026-08-20.md`'s "Follow-up investigation" section; narrative: `PIPELINE_LOG.md`'s fourth same-day addendum.

---

## Addendum 5, same day — two "not fixable" conclusions reopened; a real defect found underneath one of them

Told to keep investigating and fixing rather than stop at Addendum 4's "blanket advisory, no further action." Reopened, not re-asserted.

**Table (3/3): the earlier check stopped one level too shallow.** Addendum 4 checked Table elements for a `/C` ClassMap class, found none, and concluded there was nothing to fix. That's a different question from whether the `/Summary` this document *does* attach is valid. It is not: inspecting all three Tables directly found `/Summary` sitting as a **bare top-level key on the `StructElem` dict** — not a key ISO 32000 defines on a structure element anywhere. The spec's table attributes live inside `/A` with `/O /Table`, the same location `/Scope` needed for `TH` in the very first fix this session. This plausibly explains 100% of Tables being flagged "possibly inappropriate use" all along. **Fixed**: `tools/fix_pdf_tagging_defaults.py`'s new `fix_table_summary_attr()` promotes the existing text into a proper `/A`, additive alongside the legacy key.

**List (2/2): the ClassMap pattern that fixed `TH` applied here too, and was missed the first time.** `L` elements carry `/C /enumerate`, resolving via `/ClassMap` to `<</O /List /ListNumbering /Ordered>>` — the identical shape to `TH`'s `/Scope`. **Fixed**: `fix_list_numbering()`, same mechanism as the `TH` fix.

**This report's own numeric tests had the same blind spot the document did.** §4's table-summary test checked for the string "/Summary" anywhere on a Table object, not whether it sat in a spec-valid location — so it has reported this document's tables "pass" since the second accessibility round, on a placement that satisfies nothing per spec. Fixed in `check_structure.py` alongside the document: a new `tables_summary_not_in_A` field resolves the `/A` reference and confirms it actually contains `/O /Table` + `/Summary`. Verified able to fail, not assumed: run against the pre-fix build first, confirmed it correctly flags all three table xrefs, before being trusted to report the post-fix build clean — the same discipline this report has applied to the document from round 1 onward, now applied to its own checker.

**Formula reconsidered, not just left.** The same ClassMap-only-attribute shape exists for Formula's `/display`/`/inline` class. Checked before declining to act: `/inline` uses the identical mechanism and is 0% flagged, directly contradicting the theory that explains Table and List (where 100% of the *only* instances that exist are all flagged). Left unfixed on evidence.

**md5 `b92b19d2...` → `bf4452a1...`.** veraPDF UA-1 stays PASS, every Step 4d numeric test in §4 stays clean, `tables_summary_not_in_A` now empty. **Not yet confirmed by a live PAC run** — that requires the operator to run PAC again, which had not happened as of this md5. Stated as a well-founded hypothesis (same class of gap the TH fix closed, which PAC's own Run 2 *did* confirm effective), not as an already-proven result.
