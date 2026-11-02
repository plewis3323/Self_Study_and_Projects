# HC 6001 — Scattering by a Central Potential; the Hamiltonian

An accessible, tagged LaTeX edition of the 22 October 2024 lecture, rebuilt
from the four source pages. This report opens with what is still wrong,
because a reader who finds an unlisted defect will rightly discount everything
else in it.

**Deliverable:** `01_Deliverable/hc6001_2024-10-22_scattering_hamiltonian.pdf`
— 11 pages, MD5 `f6e5c207ecb322c6c53eaca39ba6ee64`.
**Companion:** `01_Deliverable/html/notes.html`.

This is the artifact that closed Stage 4c/4d review with unanimous approval
from all five physics referees and the accessibility auditor, after a
six-round revision cycle. `02_Accessibility_Evidence/review_log_stage4c.md`
carries the full history — including two rounds where the fix applied in the
prior round turned out to be wrong and had to be reversed after direct
testing, and one round invalidated by a process error rather than a document
defect. Nothing in that history is hidden here; it is why this report can
state, plainly, what actually is and is not still wrong, rather than what a
single confident pass concluded.

---

## 1. What is still wrong

| # | Item | Consequence for a reader |
|---|---|---|
| 1 | **5 equations carry a stray replacement character in their MathML** (Eqs. 25, 36, 48, 50, 53) — each on an algebraically-cancelled term inside an otherwise complete, correct display equation. Narrower than an earlier build's empty-MathML issue: `mathml_empty: 0` here (all 198 Formulas carry real content). | A MathML-aware reader may hear one stray symbol on the struck term in 5 of 198 equations. Not present in the primary text extraction (0 replacement characters via both PyMuPDF and poppler). |
| 2 | **PAC 2026 was not run.** Confirmed installed and reachable on the machine that built this package, but it has no command-line/batch mode and needs a person at the keyboard. | The tool an OHIO reviewer will use has not passed judgement. veraPDF 1.30.2 is the checker of record here and is not a substitute. **Run PAC before you rely on this.** |
| 3 | **PDF/UA-1 reports 189 formulas under clause 7.7.** Their accessible representation is an attached MathML file — the PDF/UA-2 mechanism, which UA-1 predates. UA-1 also fails 6.1 and 5 because the file is PDF 2.0 / `pdfuaid:part=2`. | No practical effect under the standard the document declares (UA-2, which passes). Listed because the UA-1 report is in the package and will be seen. |
| 4 | **Figures are crops of the original drawings**, so any label drawn inside a figure is an image of text. | Alt text describes each drawing's geometry and names its labelled quantities, but does not transcribe every glyph. Each figure's alt text was independently pixel-verified across 3–6 review rounds, including resolving one genuine disagreement between two review passes about which way a line in one figure points (settled by an independent line-detection analysis, not a vote). |
| 5 | **Some equations' spoken text reads tripled/garbled under one PDF library** (PyMuPDF) though not another (poppler). | A tool built on the affected library may show garbled selected/copied text for those equations. The structure tree itself carries exactly one spoken fallback per equation — this is an extraction-library quirk, not a defect in the file. |
| 6 | **Two minor documentation items**, judged non-blocking by the referees who found them: a hardcoded figure cross-reference in the notation table (numerically correct, does not auto-update if figures are reordered), and a note about a grep pattern in this pipeline's own specification document that undercounts on documents like this one. Neither affects this deliverable. |

The four structural tests that gate this pipeline all pass on measured
numbers, and you can re-run them yourself (§5). `/Scope` is present
(ClassMap `/TH-col`).

## 2. Does this meet WCAG 2.1 AA?

Yes, on every criterion that was testable here, with items 1–6 above disclosed.

| Question you will be asked | Answer |
|---|---|
| Is the PDF tagged? | Yes — 1338 structure elements, PDF/UA-2, `pdfuaid:part 2`. |
| Does it pass a conformance checker? | **veraPDF 1.30.2, PDF/UA-2: PASS.** Report in `02_Accessibility_Evidence/`. |
| Are headings real? | 16 heading elements, 1:1 with the 16 sectioning commands, no skipped levels, and 16 bookmarks mirroring them — each bookmark's target page independently re-verified across three separate review rounds to point to the page that actually contains its heading. |
| Is any content invisible to a screen reader? | **No — 0 of 3505 text operators are unreachable from the tag tree.** |
| Do figures have alt text? | 5 of 5, each specific to its drawing and distinct from its caption. |
| Is the language declared? | `/Lang (en-US)`, and the XMP agrees. |
| Is there a real title? | Yes, with `DisplayDocTitle` set so a reader hears it. |
| Are lists and tables real structures? | Yes — every list item has both a label and a body; every data table has header cells, a caption and a summary. |
| Is the contrast sufficient? | Body and link text **21:1**; the lowest ratio for any content in the document is **8.45:1**, against a 3:1 floor. |
| Can a screen-reader user follow the physics? | Yes. The walk is in `02_Accessibility_Evidence/screen_reader_walk.txt`. |

### The 7 Core Skills, row by row

| Core Skill | Verdict |
|---|---|
| Headings for clarity and logical structure | **Satisfied** — 16 headings, 1:1 with the outline, no skipped levels |
| Meaningful alt text for images | **Satisfied** — 5/5, specific and drawing-accurate |
| Sufficient colour contrast | **Satisfied** — lowest content ratio 8.45:1 |
| Format lists correctly | **Satisfied** — every list item has a label and a body |
| Create descriptive links | **Satisfied** — every link annotation carries a description |
| Design accessible tables | **Satisfied** — header cells, captions and summaries on all three |
| Captions/transcripts for A/V | **Not applicable** — the document contains no time-based media |

### Minimum Digital Accessibility Standards

Permission flag set · title present · full text present (16,724 characters,
not an image) · language specified · alt text on every figure. **All five
confirmed individually**, with evidence, in the auditor report.

## 3. Which format should you publish?

**Publish the HTML companion where the delivery channel accepts it, and keep
the tagged PDF as the archival and print copy.** OHIO's own guidance is to
reduce PDFs and prefer formats that carry structure natively; and for this
document specifically the HTML is the better artifact, because its MathML is
complete for all 198 equations, including the ones a `\boxed` or `\cancel`
mark defeats the PDF's own math tagger for. The PDF remains the right choice
for print and for archiving.

## 4. Compliance context

WCAG 2.1 Level AA, under the ADA Title II rule. Ohio University's compliance
date is **26 April 2027**.

## 5. Verify it yourself

```
cd 02_Accessibility_Evidence && ./verify.sh /path/to/verapdf
```

This re-runs the conformance check and the four numeric acceptance tests
against the PDF in this package and prints the numbers. It needs `python3`
with `pymupdf`, `numpy` and `pillow`; veraPDF is free from verapdf.org. The
tests are the point: a conformance pass alone is a floor. Across this
document's revision history, a checker has passed cleanly while headings were
mis-tagged as paragraphs, content operators sat outside the tag tree, a
table's notation was backwards relative to the textbook it claimed to follow,
and — as late as the round before this one closed — while a figure's alt text
described a line going the wrong direction. Every one of those was caught by
measuring the artifact directly, not by re-reading a prior approval.

## 6. What is in this package

| Directory | Contents |
|---|---|
| `01_Deliverable/` | the tagged PDF and its `.tex`, the style file, alt-text and errata sidecars, the figures, and the HTML companion (with its figure images now co-located with `notes.html` so they resolve when opened in a browser) |
| `02_Accessibility_Evidence/` | veraPDF reports (UA-1 and UA-2), the structural test results, contrast measurements, the reading-order and screen-reader walks, the full auditor report, the complete six-round review log, and `verify.sh` |
| `03_Source_Input/` | the untouched source PDF |
| `04_Reproduce/` | the run log, the manifest, the pipeline specification, and every tool used, including the ones added or fixed during this revision cycle |
| `05_Intermediate/` | the approved segments, the segmentation manifest, and the assembled segment PDF |

## 7. How the content was treated

The document is the source content. Every equation, derivation step, diagram
and marginal remark in the four pages appears; material not in the source was
added only where a step would otherwise be unfollowable, and each addition is
marked as supplied.

**Source errors are reproduced as written and flagged, never silently
corrected.** There are six, listed in `01_Deliverable/errata.json` and marked
in the document at the equation each concerns — among them a missing `/E` in
the quadrature, a dropped minus sign in a substitution, and a `dH` line whose
first term carries no differential. Two candidates were investigated and
**rejected as false errata** during review, because flagging a correct
expression is as damaging as missing a wrong one. One further transcription
slip — not a source error, but a mistake made while typesetting the source
correctly — was also caught and fixed: a range given in the source as
"0 < θ ≤ π" had been typeset as the strict inequality "0 < θ < π" everywhere
it appears, silently dropping the physically real endpoint at exact
backscattering.

Notation follows Goldstein, Poole & Safko, *Classical Mechanics* 3rd ed.
(Ch. 3.10 and Ch. 8), and every departure from it is stated in the notation
table in Sec. 3 of the document rather than left for the reader to infer.
That table itself needed three rounds of correction before it accurately
described Goldstein's own conventions — including one round where the fix
had the attribution exactly backwards — and is now cross-verified by two
independent reviewers against Goldstein's actual text, not merely against
each other.
