# HC 6001 — Scattering by a Central Potential; the Hamiltonian

An accessible, tagged LaTeX edition of the 22 October 2024 lecture, rebuilt
from the four source pages. This report opens with what is still wrong,
because a reader who finds an unlisted defect will rightly discount everything
else in it.

**Deliverable:** `Deliverable/hc6001_2024-10-22_scattering_hamiltonian.pdf`
— 11 pages, MD5 `85b05d31081368d8b811063456c7f769`.
**Companion:** `Deliverable/html/notes.html`.

---

## 1. What is still wrong

| # | Item | Consequence for a reader |
|---|---|---|
| 1 | **Eight equations export no MathML** (7 boxed results plus the `\xcancel` retraction). A box, and `\xcancel` over mathematics, defeat the generator. | Each of those eight Formulas carries a written-out spoken rendition on **that same** element. Ovaleq Eq. (51) is spoken but is not empty. The HTML companion's MathML for the boxed results is complete. A MathML-consuming tool reading the PDF does not get those eight. |
| 2 | **PAC 2026 was not run.** It is Windows-only; this run was on Linux. Acrobat was likewise unavailable. | The tool an OHIO reviewer will use has not passed judgement. veraPDF 1.30.2 is the checker of record here and is not a substitute. **Run PAC before you rely on this.** |
| 3 | **PDF/UA-1 reports 178 formulas under clause 7.7.** Their accessible representation is an attached MathML file — the PDF/UA-2 mechanism, which UA-1 predates. UA-1 also fails 6.1 and 5 because the file is PDF 2.0 / `pdfuaid:part=2`. | No practical effect under the standard the document declares (UA-2, which passes). Listed because the UA-1 report is in the package and will be seen. |
| 4 | **Twenty U+FFFD in Formula MathML** (7 boxed empty, 1 `\xcancel` retraction, 10 `\cancel` strokes, 2 ovaleq decoration on Eq. 51). | A screen reader may hear a replacement character at those marks. Ovaleq is not empty and has no `\cancel`. Not closed. |
| 5 | **Figures are crops of the original drawings**, so any label drawn inside a figure is an image of text. | Alt text describes each drawing's geometry and names its labelled quantities, but does not transcribe every glyph. |
| 6 | **The retraction's content-stream text is fragmented.** The tag-tree `/ActualText` is present. | A tool that extracts page text rather than walking the structure tree will not get a continuous spoken sentence there. |
| 7 | **Rebuilding from source logs 120 recovered TeX errors** in the `\tablesummary` walk (`\tl_if_in_p:Nn` undefined). | The shipped PDF already has `/Summary` on all three tables. The errors do not appear in the tagged output. |

The four structural tests that gate this pipeline all pass on measured numbers, and you can re-run them yourself (§5). `/Scope` is present (ClassMap `/TH-col`); an earlier draft of this report that said it was missing was wrong.

## 2. Does this meet WCAG 2.1 AA?

Yes, on every criterion that was testable here, with items 1–7 above disclosed.

| Question you will be asked | Answer |
|---|---|
| Is the PDF tagged? | Yes — 1292 structure elements, PDF/UA-2, `pdfuaid:part 2`. |
| Does it pass a conformance checker? | **veraPDF 1.30.2, PDF/UA-2: PASS.** Report in `Accessibility_Evidence/`. |
| Are headings real? | 16 heading elements, 1:1 with the 16 sectioning commands, no skipped levels, and 16 bookmarks mirroring them (including "Remarks on Eq. (37)" and "Chapter 8. …"). |
| Is any content invisible to a screen reader? | **No — 0 of 3406 text operators are unreachable from the tag tree.** |
| Do figures have alt text? | 5 of 5, each specific to its drawing and distinct from its caption. |
| Is the language declared? | `/Lang (en-US)`, and the XMP agrees. |
| Is there a real title? | Yes, with `DisplayDocTitle` set so a reader hears it. |
| Are lists and tables real structures? | Yes — every list item has both a label and a body; every data table has header cells, a caption and a summary. |
| Is the contrast sufficient? | Body and link text **21:1**; the lowest ratio for any content in the document is **8.45:1**, against a 3:1 floor. |
| Can a screen-reader user follow the physics? | Yes. The walk is in `Accessibility_Evidence/screen_reader_walk.txt`. |

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

Permission flag set · title present · full text present (16,064 characters,
not an image) · language specified · alt text on every figure. **All five
confirmed individually**, with evidence, in the auditor report.

## 3. Which format should you publish?

**Publish the HTML companion where the delivery channel accepts it, and keep
the tagged PDF as the archival and print copy.** OHIO's own guidance is to
reduce PDFs and prefer formats that carry structure natively; and for this
document specifically the HTML is the better artifact, because its MathML is
complete for all 187 equations including the eight the PDF cannot express.
The PDF remains the right choice for print and for archiving.

## 4. Compliance context

WCAG 2.1 Level AA, under the ADA Title II rule. Ohio University's compliance
date is **26 April 2027**.

## 5. Verify it yourself

From the kit root (`ForColleagues/`):

```
./verify.sh /path/to/verapdf
```

This re-runs the conformance check and the four numeric acceptance tests
against the PDF in this package and prints the numbers. It needs `python3`
with `pymupdf`, `numpy` and `pillow`; veraPDF is free from verapdf.org. The
tests are the point: a conformance pass alone is a floor. In the previous run
of this pipeline a checker passed cleanly three times while 16 headings were
mis-tagged as paragraphs and 24 content operators sat outside the tag tree.

## 6. What is in this package

| Directory | Contents |
|---|---|
| `Deliverable/` | the tagged PDF and its `.tex`, the style file, alt-text and errata sidecars, the figures, and the HTML companion |
| `Accessibility_Evidence/` | veraPDF reports (UA-1 and UA-2), the structural test results, contrast measurements, the reading-order and screen-reader walks, the full auditor report, and `verify.sh` |
| `Input/` | the untouched source PDF |
| kit root (`../`) | `Multi_Agent_Outline.md` (the file you feed the agent), tools, and this example |
| `Intermediate/` | page renders, approved segments, assembled segment PDF, `notes_src.tex`, review logs |

## 7. How the content was treated

The document is the source content. Every equation, derivation step, diagram
and marginal remark in the four pages appears; material not in the source was
added only where a step would otherwise be unfollowable, and each addition is
marked as supplied.

**Source errors are reproduced as written and flagged, never silently
corrected.** There are six, listed in `Deliverable/errata.json` and marked
in the document at the equation each concerns — among them a missing `/E` in
the quadrature, a dropped minus sign in a substitution, and a `dH` line whose
first term carries no differential. Two candidates were investigated and
**rejected as false errata** during review, because flagging a correct
expression is as damaging as missing a wrong one.

Notation follows Goldstein, Poole & Safko, *Classical Mechanics* 3rd ed.
(Ch. 3.10 and Ch. 8), and every departure from it is stated in the notation
table in Sec. 3 of the document rather than left for the reader to infer.
