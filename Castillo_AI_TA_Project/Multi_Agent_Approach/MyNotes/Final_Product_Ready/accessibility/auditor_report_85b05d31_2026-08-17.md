# Accessibility audit — HC 6001, Scattering by a Central Potential; the Hamiltonian

**Auditor:** Accessibility Auditor, round 3 (independent vote).
**Document:** `Final_Product_Ready/hc6001_2024-10-22_scattering_hamiltonian.pdf`
**Build audited:** MD5 `85b05d31081368d8b811063456c7f769`, 11 pages, 572403 bytes. Confirmed before measurements and again after. Unchanged.
**Standard:** WCAG 2.1 Level AA as adopted by Ohio University; PDF/UA-2 (ISO 14289-2).
**Checkers run this round:** `tools/check_structure.py`, `tools/check_contrast.py`, veraPDF 1.30.2 `-f ua2` and `-f ua1`, plus independent object/tag/HTML/geometry walks. PAC 2026 and Acrobat were not run.

Round 1 of this auditor was REVISE. Round 2 never voted. This report does not reuse PIPELINE_LOG, MANIFEST, or the previous `auditor_report.md` as evidence. Numbers below were measured on this file.

---

## What is still wrong

Stated first, because a reader who finds an unlisted defect will rightly discount everything else here.

1. **Eight equations export no machine-readable mathematics.** Identity-matched, not counted: Formula xrefs 503, 507, 587, 698, 1027, 1087, 1583 are the seven `\boxeq` results (Eqs. 9, 10, 13, 20, 34, 37, 55), and xref 1418 is the `\xcancel` retraction. Each attached MathML is an empty shell (label plus U+FFFD, or a lone `<mtext>�</mtext>` for the retraction). **Mitigation, measured on that same Formula:** each of the eight carries `/ActualText`. Ovaleq Eq. (51), xref 1542, has spoken text **and** is **not** empty — leftover character content includes `𝑝ᵢ = ∂𝐿/∂𝑞̇ᵢ` after labels and replacement characters are stripped.
2. **PAC 2026 was not run.** It is Windows-only and this run was on Linux. PAC is the tool an OHIO reviewer will use. veraPDF 1.30.2 is the checker of record here and is not a substitute for it.
3. **PDF/UA-1 fails 3 rules / 180 checks.** Clause 6.1 (`%PDF-2.0` header) and clause 5 (`pdfuaid:part` = 2) are artefacts of declaring UA-2. Clause 7.7 is **178** checks: those Formula elements have neither `/Alt` nor `/ActualText` because they carry complete MathML through `/AF`, which is how UA-2 represents mathematics. The eight empty ones are the exception and are the ones that *do* carry `/ActualText`. 187 − 8 empty − 1 ovaleq spoken = 178, which matches.
4. **Twenty U+FFFD in attached MathML, not all in boxed shells.** Eight sit in the eight empty formulas (one each). Ten sit in five `\cancelled{…}` formulas (two each: Eqs. 25, 36, 48, 50, 53). Two sit in ovaleq Eq. (51)’s wrapper `<mtext>`, which is decoration around otherwise real MathML. A claim that all twelve non-empty replacement characters are `\cancel` strokes is therefore slightly wrong; ten are cancel, two are oval. Not closed.
5. **Figures are source crops**, so labels drawn inside them are images of text. Alt text describes the geometry and names the labelled quantities but does not transcribe every glyph.
6. **`get_text()` of the page-10 retraction is fragmented** (`retract` / `e` / `d: L eq` / `u` / `a l s L of r, r-dot, p-theta, …`). The structure-tree `/ActualText` on Formula xref 1418 is the continuous string `retracted: L equals L of r, r-dot, p-theta`. Disclosed rather than claimed as continuous prose. A tag-tree walker hears the fallback; a raw content-stream extractor does not.

`/Scope` is **present**: all 7 TH carry `/C /TH-col`, and ClassMap (xref 1691) defines `/TH-col << /O /Table /Scope /Column >>`. `/Summary` sits on the three Table elements (xrefs 809, 1234, 1277), not on TH.

Caption–`\toprule` gaps, measured from the last short caption-text span to the first horizontal rule below it: **11.0 / 10.5 / 8.4 pt** (10.96 / 10.48 / 8.35). All ≥ 6. The pipeline’s “8.3” for Table 3 is a one-tenth rounding; the geometry is 8.35 pt.

---

## 1. The four Step 4d numeric tests

Measured by `python3 tools/check_structure.py … --alt Final_Product_Ready/alt_text.json --sections 16` (16 sectioning commands in the `.tex`).

| # | Test | Result | Acceptance | Verdict |
|---|---|---|---|---|
| 1 | Heading inventory | **16** H-elements (H1 4, H2 10, H3 2) against **16** sectioning commands, 0 skipped levels | 1:1 with the outline | **PASS** |
| 2 | Content reachability (MCID walk) | **0 unreachable** of **3406** text operators; 23 decoration, 3383 reachable | zero unreachable | **PASS** |
| 3 | Artifact audit | **132** artifact frames, unclassified; **0** carry words; **0** bury tagged content | nothing meaningful is an artifact | **PASS** |
| 4 | Figure reading position | 5 figures at **6.7 / 15.9 / 17.8 / 33.0 / 69.3 %** | none clustered at the end | **PASS** |

Outline bookmarks: **16**, titles matching the heading structure, including `Chapter 8. The Hamiltonian…` and `Remarks on Eq. (37)`.

## 2. Machine check

- **veraPDF 1.30.2, `-f ua2`:** PASS. Profile “PDF/UA-2 + Tagged PDF”; `isCompliant="true"`; 1727 rules passed, 0 failed; 59249 checks passed, 0 failed. Matches the existing `verapdf_ua2.xml` / `.txt` in this folder; those files were not overwritten.
- **`-f ua1`:** FAIL, 3 rules / 180 checks — analysed in item 3 above. Matches the existing `verapdf_ua1.xml` / `.txt`; not overwritten.
- **PAC / Acrobat:** not run.

## 3. The MDAS five

| # | Check | Evidence | |
|---|---|---|---|
| 1 | Permission flag set | not encrypted; PyMuPDF `permissions` has the accessibility bit; no extraction restriction | PASS |
| 2 | Title present | `/Title` "Scattering by a Central Potential; the Hamiltonian"; `/DisplayDocTitle true` | PASS |
| 3 | Full text, not image-only | **16,064** characters extracted across 11 pages | PASS |
| 4 | Language specified | catalog `/Lang (en-US)` | PASS |
| 5 | Alt text on every figure | **5/5**, each matching `alt_text.json`, none equal to its caption | PASS |

## 4. The 7 Core Skills

| OHIO Core Skill | Verdict | Evidence |
|---|---|---|
| Headings for clarity and logical structure | **Satisfied** | 16 H-elements 1:1 with the outline, 0 skipped levels, 16 bookmarks |
| Meaningful alt text for images | **Satisfied** | 5/5 specific and drawing-accurate, distinct from captions. fig1 names the blue path vs black axis in words (WCAG 1.4.1) |
| Sufficient colour contrast | **Satisfied** | body **21:1**; figure blue pen **8.45:1**. Lowest *content* ratio 8.45:1 against a 3:1 non-text floor |
| Format lists correctly | **Satisfied** | L 2, LI 6, Lbl 16, LBody 6; every LI has Lbl and LBody |
| Create descriptive links | **Satisfied** | 36/36 link annotations carry `/Contents` (e.g. "Go to destination equation.9") |
| Design accessible tables | **Satisfied** | 3 data tables, 7 TH with `/C /TH-col`, caption and `/Summary` on each Table |
| Captions and transcripts for A/V | **Not applicable** | no time-based media |

## 5. The three items no tool decides

**Logical reading order — pass.** Figures sit at 6.7–69.3 % of the tag tree, not dumped at the end. Split sentences from the previous build are re-knit in the content stream: "Eq. (18) then becomes" and "Substituting into Eq. (9) gives" are present as continuous strings; the old fragments "this becomes" and "and substituting into Eq. (9)" are absent. A structure-tree walk of the Rutherford section (H1 xref 1008 through Remarks H2 xref 1091) encounters the derivation, then Formula 1027 (`s equals the absolute value of Z Z prime e squared…`) and Formula 1087 (`sigma of theta equals one quarter times…`) each with a single `/ActualText` on that Formula — not a nested 4× copy. The retraction passage’s content-stream text is fragmented; the tag-tree ActualText is present (item 6 above).

**Colour contrast — pass, with the excluded layer disclosed.** PDF body text is rgb(0,0,0) at **21.00:1** (15369 chars). Figure crops: four are black pen at 21.00:1; `scat_fig1_beam_ring.png` worst content layer is blue pen rgb(51,51,204) at **8.45:1**. Printed ruling rgb(52,132,210) is **3.91:1** and is excluded from the verdict as paper, not content. Greyscale blue/black separation in fig1 is **2.49:1**, so the distinction is named in the alt text (WCAG 1.4.1).

**Table summary — pass.** `/Summary` is on Table xrefs **809, 1234, 1277** and on no TH. Summaries describe orbit type by energy sign; classical vs quantum total cross section; and this document’s symbols vs Goldstein, Poole & Safko. Caption–`\toprule` gaps: **11.0 / 10.5 / 8.4 pt**, all ≥ 6.

## 6. Math

187 `Formula` elements; 151 distinct MathML files attached through `/AF`.

Empty MathML, identity-matched (not a count comparison):

| Formula xref | Eq. | Fallback on that Formula |
|---|---|---|
| 503 | (9) | "sigma of theta equals s over sine theta…" |
| 507 | (10) | "sigma sub T equals the integral of d Omega…" |
| 587 | (13) | "theta equals the absolute value of pi minus 2 psi" |
| 698 | (20) | "theta of s equals the absolute value of pi minus twice the integral…" |
| 1027 | (34) | "s equals the absolute value of Z Z prime e squared over 2 E…" |
| 1087 | (37) | "sigma of theta equals one quarter times, Z Z prime e squared…" |
| 1418 | retraction | "retracted: L equals L of r, r-dot, p-theta" |
| 1583 | (55) | "partial H by partial p i equals q dot i; …" |

**0 empty without a fallback on that Formula.** 9 Formulas carry `/ActualText` (the 8 empty plus ovaleq Eq. 51 / xref 1542). Ovaleq is not in the empty list. Replacement characters: 20 total = 8 empty + 10 cancel + 2 oval.

## 7. HTML companion

Held to the same WCAG 2.1 AA bar. Measured on `Final_Product_Ready/html/notes.html`:

- **187** `<math` elements; **0** rasterised equations.
- Heading levels **1 / 2 / 3 / 4** with no skipped levels (document title H1, then § as H2, …, 4.1.1/4.1.2 as H4).
- **5/5** `<img>` with alt from the sidecar; `img { max-width: 100%; height: auto }`.
- **3** data tables (`class='tabular'`), each with `<caption>` and real `<th scope='col'>`. Header cells: 7 real (Energy/Orbit; Theory/Total cross section; Used here / Goldstein / Quantity) plus 3 empty `\noalign` rows. 48 additional `class='equation' role='presentation'` tables are layout, not data.
- Goldstein is named (Table 3 caption and the "Goldstein / elsewhere" header). Chapter 8 appears in the §4 heading: "4 Chapter 8. The Hamiltonian and Hamilton’s equations of motion".
- Lists: 2 `<ol>`, 6 `<li>`.

---

## Verdict

**VERDICT: APPROVE**

The four mandatory numeric tests pass on measured numbers. veraPDF UA-2 passes. Table `/Summary` is on Table, `/Scope` is in the ClassMap, empty MathML is identity-matched to spoken fallbacks, ovaleq Eq. (51) is not treated as empty, caption–rule gaps all clear 6 pt, contrast clears with the ruling exclusion stated, and the HTML companion matches the PDF on MathML count and heading integrity. The residual list above is the list I would put in front of an OHIO reviewer; I would sign this file with those limitations disclosed. PAC remains unrun and is the one check this Linux audit cannot substitute.
