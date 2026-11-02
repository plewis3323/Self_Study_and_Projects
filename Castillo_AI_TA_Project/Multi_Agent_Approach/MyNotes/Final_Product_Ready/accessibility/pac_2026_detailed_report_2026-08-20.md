# PAC 2026 detailed checkpoint report — transcribed 2026-08-20

PAC 2026 (v26.1.0.0, Windows) exports a one-page summary PDF
(`hc6001_2024-10-22_scattering_hamiltonian_PAC_UA_Report.pdf`, in
`TA_Tasks/`) that has no checkpoint-level detail — every finding below came
from the operator expanding PAC's "Results in Detail" panel in the GUI and
screenshotting it, since PAC has no CLI/batch export of that view. This file
is the durable, stored transcription of those screenshots so the finding
survives after the screenshots themselves age out of an email attachment
folder. See `MANIFEST.json`'s `accessibility.pac_2026_review` for the
synthesized verdict and `PIPELINE_LOG.md`'s 2026-08-20 "same day" entry for
the narrative.

**Target file:** the frozen `ForColleagues/Worked_Example/Deliverable/`
copy, md5 `85b05d31081368d8b811063456c7f769` (per the accreport HTML's own
embedded `pdf-source` comment). **Not** the round-6 build directly — every
finding below was independently re-verified against the round-6 PDF
(md5 `f6e5c207...`) via pikepdf before being acted on, since the two builds
share the same toolchain but are not the same file.

**PAC's own caveat, verbatim from its "Unsupported PDF version" dialog:**
"This document is based on the PDF standard 2.0. PAC currently fully
supports documents up to and including PDF standard 1.7. ... It is possible
that errors or unreliable results may occur." Weighed accordingly below —
findings independently confirmed via direct PDF inspection are marked as
such; PAC's own characterization alone was not treated as sufficient.

## Top level

PDF/UA-1: 17490 Passed / 75 Warned / 196 Failed. WCAG: 20954 / 75 / 196.
Quality: 25 / 14 / –.

## Logical Structure (1395 / 75 / 196)

| Checkpoint | Passed | Warned | Failed |
|---|---:|---:|---:|
| Structure Elements | 114 | – | 7 |
| Structure tree | 518 | 75 | – |
| Role mapping | 713 | – | – |
| Alternative Descriptions | 50 | – | 189 |

### Structure Elements → Tables → Table header cell assignments (7 Failed)

All 7 failures are **"Table header cell has no associated data cells"** —
one per `TH` element in the document (3 tables, 7 header cells total).
Screenshot showed the checkpoint expanded with 7 identical-title rows, one
highlighted against page 5's "Energy / Orbit" table.

**Independently confirmed** (pikepdf against both the 85b05d31 and f6e5c207
builds): all 7 `TH` StructElems carry `/C /TH-col` and no `/A`; the
document's own `/ClassMap` resolves `/TH-col → <</O /Table /Scope
/Column>>`. Spec-conformant ISO 32000-2 indirection; PAC does not appear to
resolve it. **Fixed** — see `pac_2026_review` in `MANIFEST.json`.

### Structure tree → "Part" structure elements (1 Passed / 57 Warned)

All 57 warnings: **"Possibly inappropriate use of a 'Part' structure
element."** Screenshot showed the category collapsed (57 count, not
individually expanded) alongside a passing "Document" (1) and other
passing categories (Sect 18, Div 12, H1 4/H2 10/H3 2).

**Independently confirmed:** `RoleMap /text-unit → /Part`; every one of the
58 `text-unit`-tagged StructElems in the round-6 PDF is a paragraph wrapper
(`\AssignStructureRole{para/semantic}{text-unit}` in
`latex-lab-testphase-names.sty`; `text-unit, Part, pdf2,` in
`tagpdf-ns-latex-lab.def`, the kernel's own default table — not a
`goldsteinnotes.sty` or transcription choice). **Fixed** — remapped to
`/P`.

### Structure tree → "Note" structure elements (– Passed / 8 Warned)

All 8 warnings: **"Possibly inappropriate use of a 'Note' structure
element."** Screenshot's viewer pane highlighted Figure 2's caption region
(page 2) as one instance.

**Independently confirmed:** `RoleMap /float → /Note`; the document's raw
`element_types` count shows exactly 8 `float`-tagged elements — one per
LaTeX float environment (5 `figure` + 3 `table` = 8), the kernel's own
`float, Aside, pdf2,` default (resolving through to `/Note` in this
document's compiled RoleMap) rather than anything hand-authored. **Fixed**
— remapped to `/Div`.

### Structure tree → "Caption" structure elements (2 Passed / 8 Warned)

All 8 warnings: **"Possibly inappropriate use of a 'Caption' structure
element."** Not investigated — no root cause traced, so nothing was fixed.
Disclosed in `MANIFEST.json known_gaps`.

### Structure tree → "P" structure elements (113 Passed / 2 Warned)

2 warnings: **"Possibly inappropriate use of a 'P' structure element."**
Screenshot's viewer pane highlighted the title-block text ("the
Hamiltonian", byline) on page 1 as one instance. Not investigated. Disclosed
in `MANIFEST.json known_gaps`.

### Alternative Descriptions (50 Passed / 189 Failed)

- "Alternative text for 'Figure' structure elements": 5/5 Passed.
- "Alternative text for 'Formula' structure elements": 9 Passed / 189
  Failed, each a **"Alternative text missing for 'Formula'"** row.
  Screenshot's viewer pane highlighted Eq. (4), `s = ℓ/√(2mE)`, as one
  instance.

**Independently confirmed:** exact match to `structure_tests.json`'s own
`math.formula_elements: 198` minus `math.formulas_with_alt_or_actualtext:
9` = 189. Already disclosed (clause 7.7, `MANIFEST.json known_gaps`).

**UPDATE, same day, second addendum:** this is not merely disclosed anymore
— the root cause (declaring `pdfstandard=ua-2`, whose `/AF`-only math
tagging UA-1's clause 7.7 does not recognize as alt text) was closed by
switching the declared standard to `ua-1`. All 198 Formulas now carry
`/Alt` or `/ActualText`; veraPDF UA-1 flipped FAIL→PASS. See
`MANIFEST.json`'s `toolchain.standard_change` and `PIPELINE_LOG.md`'s
second 2026-08-20 "same day" entry. Residual, disclosed: 189 of the 198
get the kernel's auto-generated raw-LaTeX-source `/Alt`, not spoken math —
still non-empty and conformant, but lower quality than the 9 hand-authored
`\formulaalt` renditions.

## WCAG → 1 Perceivable → 1.3 Adaptable → 1.3.1 Info and Relationships

All sub-checks Passed except **"Table header cell assignments": 7 Failed**
— the same 7 `TH` findings as above, surfaced a second time under WCAG's
own tree. Notably, everything upstream of it in this same checkpoint
group Passed cleanly, including "Mapping of characters to Unicode: 4568
Passed" — i.e. PAC's character-encoding check on *this* file did not fail
under PAC (unlike Adobe Acrobat's separate check on the same file, which
did fail "Reliable character encoding" — see below). The two checkers
disagree here; both are recorded rather than one being preferred silently.

## WCAG → 4 Robust (1182 Passed / 75 Warned)

The same 75 structure-tree warnings (Part/Note/Caption/P) re-surface here
under WCAG's robustness checkpoint rather than a new finding.

## Quality (25 Passed / 14 Warned)

Not expanded in the screenshots taken; not investigated this round.

## Adobe Acrobat accessibility checker (separate tool, same 85b05d31 file)

Run by a colleague; report is `TA_Tasks/hc6001_2024-10-22_scattering_hamiltonian.pdf.accreport.html`, 27 Passed / 1 Failed / 3 Needs-manual-check / 1 Skipped. The 1 Failed:
**Character encoding** ("Reliable character encoding is provided") —
matches `Multi_Agent_Outline.md` Step 4d's own standing note that this is
"the rule this toolchain actually fails." Already known. No action.

---

# Run 2 (same day) — PAC re-run against the fixed UA-1 build, md5 `b92b19d2...`

Summary report: `pac_2026_summary_report_2026-08-20_run2.pdf`. Detailed
checkpoint screenshots this time came pre-sorted by the operator into
`Formula/` (52 files), `P/` (94), `Table/` (3), `L/` (2), `Whitespace/` (6)
— 157 total, transcribed below (PAC's own summary states 151 Structure-tree
Warned; the small discrepancy is not reconciled, e.g. `Table_002`/`Table_003`
may overlap with an already-counted `L` or `Whitespace` instance, not
investigated further since it doesn't change the finding).

**Top level: 0 Failed everywhere.** Structure elements 7→**0**, Alternative
Descriptions 189→**0** (239/239 pass — same total item count as before, so
this is the same population fully closing, not a narrower check). Overall
verdict: red "not compliant" → yellow "it's possible that some PDF/UA
requirements aren't met." Both fixes from Run 1 confirmed working, by the
same tool that reported the original failures.

**Structure tree Warned rose 75→151 despite the Part/Note fix removing 65
of the original 75.** Hypothesis tested before any further `.tex` edit,
per this file's own practice of independent verification: that the 189
formulas now carrying the UA-1 switch's auto-generated raw-LaTeX `/Alt`
were tripping a PAC content-quality heuristic. **Disproven by direct
evidence:**

- `Formula_007_page-2.png`: "Possibly inappropriate use of a 'Formula'
  structure element", highlighting Eq. (9) — `σ(θ) = s/sinθ |ds/dθ|`,
  i.e. `eq:sigma-general`, one of the 8 boxed equations with a
  hand-authored `\formulaalt` spoken rendition since the very first
  accessibility work on this document.
- `Formula_008_page-2.png`: same warning, Eq. (10) — `σ_T = ∫dΩ σ(Ω)`,
  `eq:sigma-T-def`, also hand-authored.

If alt-text quality were the driver, these two — with objectively the best
alt text in the document — would be clean. They are not. Checked instead
against the PDF's own structure tree (pikepdf, not assumed): **52 `/display`-
class Formula elements, 146 `/inline`-class. PAC flags 52/52 display, 0/146
inline** — exact match to the display/inline split, zero correlation to
alt-text content. Same 100%-of-population pattern for Table (3/3,
`Table_001_page-5.png` flags a completely ordinary 2-column/3-row Energy/
Orbit table) and L (2/2). `/display` and `/inline` resolve via `/C`+
`/ClassMap` to pure layout hints (`<</O /Layout /Placement /Block>>` vs
`/Inline`) — the same indirection mechanism as the already-fixed TH-scope
issue, but inline formulas use the identical mechanism and are 0% flagged,
so this is not a ClassMap-resolution gap either.

**Conclusion:** a checkpoint firing on literally every instance of a role
regardless of content is not measuring a property of that content — it
reads as a blanket "confirm this Formula/Table/List is used correctly"
advisory PAC applies to every block-level instance of those three roles,
structurally the same category as `Multi_Agent_Outline.md`'s own "three
items no tool decides" (reading order, color contrast, table summary).
**No further `.tex` edit follows from this** — writing spoken-math alt
text for the other 44 display formulas was budgeted and not done, because
the hypothesis that would have justified it was tested first and failed.

**P (94/172) — only partially explained, genuinely open.** At least 58 are
the same paragraphs the Part-remap moved the warning onto (not eliminated
it, relocated it) plus the 2 pre-existing title-block instances (`P_004`:
the "22 October 2024" date line). The remaining ~34 are not confirmed;
sampling (`P_009`: "The volume element and the solid angle are", a
one-line lead-in immediately before a display equation) suggests very
short single-sentence paragraphs may be a factor, common in this document's
style of terse lead-ins before equations, but this is not verified against
all 94 instances and should not be treated as established.

**Whitespace (6)** — "Tagged text consists of only whitespace, and its
location can only be approximated" — plausibly related to the already-
disclosed `\noalign`/`/Summary`-parking leftover-empty-row cosmetic issue
(HTML companion side), not independently confirmed on the PDF side.

---

# Follow-up investigation (same day, continued) — closing out every remaining category

The three items left open above were each investigated further rather than left as guesses.

## Table (3/3) and L (2/2): confirmed blanket, not content-dependent

Checked all 3 Table screenshots and both L screenshots, not just one each.
`Table_001` (2-col/5-row Energy/Orbit table), `Table_002` (2-col/3-row
Classical/Quantum table), `Table_003` (3-col/8-row notation table) — every
table regardless of size or column count is flagged. `L_001` (2-item
enumerate) and `L_002` (4-item enumerate) — both lists regardless of item
count are flagged. This rules out a size/complexity-dependent cause and
confirms the blanket-advisory read from the Formula finding generalizes:
**every block-level Table and every List in the document is flagged,
100% of population, independent of content.**

## Whitespace (6) — root cause confirmed, tied to the known `\noalign` mechanism

None of the 6 Whitespace screenshots carry a location marker (PAC states
outright: "its location can only be approximated"), but all 6 land on pages
**5, 5, 8, 8, 9, 9** — exactly the document's 3 table pages, 2 instances
each. This matches `\tablesummary`'s implementation in `goldsteinnotes.sty`
(a `\noalign{\tablesummary{...}}` row inserted immediately after
`\begin{tabular}` specifically so `/Summary` lands on the `Table` element
rather than the first `TH` cell) — the same mechanism already disclosed as
leaving "one leftover empty `<tr>`" in the HTML companion. This is its PDF-
side counterpart: an essentially-empty, whitespace-only tagged span, once
per table, that PAC cannot pin a page location to. **Root cause confirmed,
not fixed**: redesigning `/Summary` attachment to avoid this would touch
markup inside all 3 already-approved tables, for a Warned (not Failed),
narrow, cosmetic outcome — the same trade-off already accepted for the
HTML-side twin of this issue.

## P (94/172) — now substantially explained, not left as a guess

**6 of the 94 are the same `\noalign` artifact, double-counted.** The `P/`
folder contains 6 files with no page number at all
(`P_041/042/073/074/076/077_page-none.png`, blank white images, no
highlight) — and their position in the file sequence places them
immediately adjacent to pages 5, 8, and 9 (2 each), the identical pattern
as the Whitespace group. These are very likely the *same 6 document
locations*, counted once under PAC's generic "Whitespace" checkpoint and
again under its role-specific "P" checkpoint — not 12 independent defects,
6 unique ones counted twice.

**At least 58 are the Part→P relocation** from the earlier RoleMap fix
(documented in Run 1/Run 2 above) — these paragraphs were flagged as
"inappropriate Part" before, now flagged as "inappropriate P" instead; the
fix changed which role gets questioned, not whether one is.

**The remainder (~30) trace to a real, consistent content pattern, checked
against 7 direct samples, not asserted from 1 or 2:**

| Sample | Flagged text |
|---|---|
| `P_004` | "22 October 2024" (title-block date line) |
| `P_009` | "The volume element and the solid angle are" |
| `P_017` | "The two signs of the force give the two geometries of Figs. 2 and 3." |
| `P_030` | "Eq. (18) then becomes" |
| `P_050` | "What is needed now is ψ = θ̃(r→∞) = θ̃(1/r→0). In the repulsive case θ = π−2ψ, so ψ = (π−θ)/2 and" |
| `P_060` | "Substituting into Eq. (9) gives" |
| `P_090` | "gives" (one word) |

Every one of these is a short lead-in or transition clause immediately
adjacent to a display equation — exactly this document's (and physics
notes generally) prose style of introducing nearly every numbered equation
with a terse clause of its own paragraph ("Therefore", "so that", "which
gives", "Substituting X into Y gives"). This is a real, traceable pattern,
not a guess dressed as one — but it is not a defect: these are legitimate,
correctly-punctuated sentences, just short ones, and the document has this
structure on essentially every page because it has a display equation on
essentially every page. **Not fixed, deliberately**: closing it would mean
merging dozens of these lead-in clauses into their following equations
throughout a document that already passed 6 rounds of physics review —
a substantial rewrite of approved content for a Warned, not Failed,
advisory-tier finding.

## Character encoding (Adobe's one remaining Failed item) — re-tested on the current build, found clean

Adobe's "Reliable character encoding" failure was reported against the
*old, frozen* `85b05d31...` copy and cited as `Multi_Agent_Outline.md`'s
already-known toolchain limitation. Re-tested here, not just re-cited:
extracted the full text of the **current** `b92b19d2...` build with two
independent extractors (PyMuPDF and poppler's `pdftotext -enc UTF-8`) and
scanned for U+FFFD replacement characters and Private-Use-Area codepoints
(U+E000–U+F8FF), the signature of a ToUnicode gap. **Zero found by either
extractor**, across all 14,966 extracted characters. Every font in the
document (`LMRoman10/12/17`, `LatinModernMath`) carries a `/ToUnicode`
CMap, checked directly via pikepdf. This does not prove Adobe's checker
would now report a clean pass — its methodology may inspect font CMap
completeness more strictly than a text-extraction scan can replicate, and
it has not been re-run against this build — but two independent, capable
extractors finding a completely clean result is real evidence the gap this
finding pointed at, if it ever affected this specific build, does not
reproduce now. **Recommend**: re-run Adobe Acrobat's checker against
`Final_Product_Ready/hc6001_2024-10-22_scattering_hamiltonian.pdf`
(`b92b19d2...`) specifically, not the frozen `85b05d31...` copy, for a
definitive answer neither extractor can fully substitute for.
