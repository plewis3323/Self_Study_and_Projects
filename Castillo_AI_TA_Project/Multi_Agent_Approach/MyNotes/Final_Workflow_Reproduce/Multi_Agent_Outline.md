# Multi-Agent Pipeline: Handwritten Notes → Accessible LaTeX PDF

## Run this file

**This file is the process.** An operator opens an agent platform that can run
shell commands, read and write files, and see images on this machine (Cursor
Agent, Claude Code, Codex CLI — not a browser chat), points the agent at the
directory containing this file, and sends this markdown. That is the whole
interface. Do not wait for a second prompt.

You are the Prime Agent. Read this file completely. It is the specification,
and where it conflicts with your defaults, it wins. Then execute it.

1. **Working directory** is the folder that contains this file. `tools/` and
   `input/` (also accept `Input/`) live next to it.
2. **Inputs.** Every PDF in `input/` / `Input/`. One PDF per lecture topic;
   the pipeline emits exactly one tagged document per input and never merges
   or splits. If that folder is empty, stop and tell the operator to drop
   PDFs there.
3. **Toolchain probe, before Stage 0.** Compile a probe document (one
   equation, one list, one table, one figure) three times with LuaLaTeX and
   inspect the **output PDF**, not the log, for `/Formula`, `/L`, `/Table`,
   `/TH` and `/Alt`. If any is missing, **stop**. Do not engineer a
   workaround. `pdflatex` is forbidden.
4. **Execute Stages 0 through 5 in order**, using the scripts in `tools/`
   rather than reimplementing them — the **Command Reference** section below
   gives every invocation in order, as it actually ran. Call
   `make_accessible.py` with `--modern`. Compile with LuaLaTeX, three passes.
5. **Review loops are the point, not paperwork.** Spawn reviewer agents as
   genuinely independent subagents. Do not show them each other's findings.
   Do not close a loop until every reviewer returns APPROVE. Write every
   round — including the approving round — into the review log. Each round
   re-checks the previous round's fixes. A first-round unanimous APPROVE
   means the reviewers were too soft: tell them to find at least three
   concrete defects each, with file and line, and run the round again.
6. **Stop and ask the operator before you:** settle on the reference
   textbook (Stage 4a); act on anything you believe is an error in the
   source physics; depart from this specification in any way.
7. **Report numbers, not adjectives.** Every accessibility claim is the
   unedited output of a command you ran. Freeze each review-round PDF and
   record its MD5. One of the five Stage 4c referees is adversarial: that
   referee's job is the gap between what the logs claim and what the frozen
   PDF measures.

Then continue with the rest of this file as the binding spec.

---

## Project Goal

Build a reusable multi-agent framework that converts handwritten notes (paper, whiteboard, or chalkboard photos/scans in PDF form) into legible, well-segmented, LaTeX-compiled PDF outputs that are **accessible** — tagged for screen readers, not merely visually correct.

"Accessible" is a hard requirement of the deliverable, not a polish item. A PDF that looks right but carries no structure tags, no figure alt text, and no machine-readable math does **not** satisfy this project's definition of done. The binding standard is **WCAG 2.1 Level AA** and the corresponding PDF standard is **PDF/UA (ISO 14289)** — this pipeline's own defaults, chosen because they are the standard most institutions already require or are moving toward, not because of any one institution. The governing rules are set out in the next section; they are not background reading, they are the acceptance bar. That section separates the **universal core** (applies wherever you run this) from a fully **worked institutional profile** (Ohio University, this kit's origin) that you swap out for your own institution's equivalent.

This document is the master plan. Feeding it to an agent that can act on this machine **is** the pipeline. It is meant to be **edited and reused** — swap the PDFs in `input/`, the reviewer specialty, or the reference textbook; leave the stages and the accessibility layer alone.

**Status:** this specification is proven, not aspirational. `Example_Deliverable_Directory/` in this kit is a complete run of this exact pipeline on `Example_Input_Directory/`'s source lecture, carried through six rounds of review to a tagged, conformant PDF plus its HTML/MathML companion. Requirements below that cite a concrete failure — a mis-tagged heading, an empty MathML shell, a figure appended at the end of the document — describe a defect this pipeline has actually had to catch and close, not a hypothetical; they are evidence for why the rule exists, not a log you need to go consult. This file assumes no prior run of any kind — read it top to bottom and execute it fresh.

---

## Governing Standard — Institutional Accessibility Requirements

This pipeline is not free to invent its own definition of "accessible." But it is also not tied to any one institution's paperwork — Stages 1–5 are identical no matter who receives the output. This section is in two parts. First, the **universal core**: the legal and technical standard that applies wherever you run this. Second, a **worked institutional profile** — Ohio University, this kit's origin — kept in full rather than trimmed to an abstract, so a colleague porting the pipeline to a different institution has a complete example to copy the shape of, not a description of one. Source documents for the profile are archived in `refs/OU-accessibility-sources/` and indexed in **Appendix: Worked Institutional Profile** at the end of this file; build the equivalent for your own institution the same way.

**If you are running this pipeline for an institution other than Ohio University:** read the institutional profile once for its shape (a legal basis, a faculty-facing checklist, a named checker, a format preference, a minimum floor), then replace its content with your own institution's policy documents. Leave the universal core and every technical stage (1 through 5) untouched — none of it is Ohio-specific.

### Universal core — applies regardless of institution

**Legal basis and standard.** In the United States, the DOJ's ADA Title II rule (April 24, 2024) makes **WCAG 2.1 Level AA** the technical standard for web and mobile content of state and local government entities, which includes public universities. The DOJ Interim Final Rule of April 20, 2026 extended compliance dates by one year: entities serving 50,000+ move to **April 26, 2027**, smaller and special-district entities to **April 26, 2028**. *Requirements did not change with the extension; only the dates did.* WCAG 2.1 AA is supplemented by **WAI-ARIA 1.2** and **WCAG2ICT** for non-web content — WCAG2ICT is the clause that makes a standalone PDF in scope at all, since WCAG itself is written for web pages, not documents. A private institution, or one outside the US, may bind to a different instrument (the EU's EN 301 549, the UK's PSBAR, or its own internal policy) — the technical layer below (PDF/UA, the Step 4d numeric tests) is standard-agnostic and travels regardless; only the legal citation and the deadline change.

**The corresponding PDF standard is PDF/UA (ISO 14289)** — see the UA-1 vs UA-2 decision in Toolchain Prerequisites below, which does not depend on institution.

**Any institutional checklist is a floor, not a target.** Whatever minimum list your institution names (Ohio University's is reproduced as MDAS below), a document can pass every item on it and still be unusable, exactly as described in Operating Principle 10.

### Worked institutional profile — Ohio University

Everything below is Ohio University's specific packaging of the universal core above. It is kept in full as a template: swap it out wholesale for your own institution's equivalent documents and change nothing else in this file.

Ohio University falls in the DOJ's first compliance tier — **April 26, 2027**. Its OIT has formally adopted WCAG 2.1 AA (all 50 A + AA success criteria) as the university's primary technical standard.

**The 7 Core Skills.** OHIO's faculty-facing framing of the standard is a subset of WCAG called the *7 Core Skills for Digital Accessibility*. Every one of them has a concrete pipeline owner, and no stage may claim completion while its skill is unaddressed:

| OHIO Core Skill | Where this pipeline satisfies it |
|---|---|
| Use headings for clarity and logical structure | Stage 4b real `\section`/`\subsection`; verified by the Step 4d heading inventory |
| Write meaningful alt text for images | Stage 1 `alt_text.json` drafted at crop time; enforced at build; audited in 4d |
| Maintain sufficient color contrast | Stage 1 crop legibility check and Stage 4b link/rule colors; measured in 4d |
| Format lists correctly | Stage 4b native `itemize`/`enumerate` → `L`/`LI`/`Lbl`/`LBody`; checked in 4d |
| Create descriptive links | Stage 4b link-text rule; checked in 4d |
| Design accessible tables | Stage 4b header rows + summary; checked in 4d |
| Accurate captions and transcripts for A/V | Not applicable — this pipeline emits no time-based media. State that explicitly rather than leaving the row blank. |

**OHIO's document-format position, and what it means for the deliverable.** OIT's guidance is, in order: *reduce unnecessary PDFs; choose a different format (Canvas page, Word, web page) when creating new content; improve the PDFs that must remain; build accessibility in from the start.* A scanned PDF is named as the worst case — OCR must be run before remediation can even begin. This pipeline deliberately sits at the top of that hierarchy rather than the bottom: it does not OCR-and-patch a scan, it **re-authors the content from source**, which is why the HTML + MathML companion is a required sibling and not a nicety. Where a recipient can take HTML, **hand them the HTML as the primary artifact and the tagged PDF as the archival copy** — that ordering is what OHIO's guidance actually asks for, and it should be stated in the Stage 5 report rather than silently decided.

**No safety net.** Ohio University provides **no centralized in-house PDF remediation service**; departments that need a document remediated must pay an external vendor. Every defect this pipeline ships is therefore either a cost to someone downstream or a barrier that never gets removed. This is the practical argument behind Operating Principle 9 — remediation is not available as a fallback, so "accessible by construction" is the only route that works.

**Institutional tooling.** OIT names **PAC 2026** (PDF Accessibility Checker, distributed through Company Portal, **Windows only**) as the recommended PDF checking tool. veraPDF remains this pipeline's automation backbone because it is free, cross-platform and scriptable, but PAC 2026 is what an OHIO reviewer will run, so a PAC pass is the acceptance check whenever a Windows machine is available. Where it is not, the run log must say so plainly rather than implying PAC was used.

**Minimum Digital Accessibility Standards (MDAS)** — the five checks OHIO applies to any submitted PDF, and the floor beneath everything else in this document:

1. PDF accessibility permission flag is set.
2. PDF includes a title.
3. PDF includes full text (not image-only).
4. Text language of the PDF is specified.
5. Figures and images include alternative text.

MDAS is a *floor*, not a target — a document can pass all five and still be unusable, exactly as described in Operating Principle 10. Note also OHIO's ETD practice of **attaching the accessibility report to the document itself** and submitting the two together; this pipeline follows it (Step 4d).

---

## Operating Principles

These apply to every stage of the pipeline:

1. **Speed with precision.** The job should run relatively fast without sacrificing quality. Parallelize wherever stages or inputs are independent; reserve careful sequential work for the steps that actually need it (review loops, final compilation).
2. **Batch inputs, parallel subagents.** The pipeline accepts **multiple input PDFs at a time**. The Prime Agent should spawn **as many subagents as needed** to run the process chain concurrently across inputs (e.g., segment/review each source PDF in parallel), keeping the run both fast and high-quality.
3. **Archive before you run.** If directories from old or previous jobs exist (`segments/`, `assembled/`, `Final_Product_Ready/`, etc.), **archive them first** (e.g., move into a timestamped `Run_Archive/` folder), then execute the whole process fresh.
4. **Source content dominates.** The final LaTeX PDF is **overwhelmingly the content of the source notes themselves** — every equation, derivation step, diagram, and remark that appears in the source must appear in the output. Material not present in the source is added **only when it is genuinely needed** to make a step followable, and when added it must be **very concise** (a clause or a single short sentence). If a passage can stand without the addition, leave the addition out.
5. **No meta-introduction.** The final notes document must **not** open with an intro describing what the agents did or how the pipeline works — it gets right into the notes.
6. **Self-contained voice — never reference the source medium.** The document must read as a standalone physics text. It must **never** refer to where the material came from. Phrases such as *"in the original notes,"* *"on the board,"* *"as written in the notes,"* *"the notes show,"* *"from the lecture,"* *"the handwritten page,"* *"as drawn above in the notes,"* or any equivalent are **forbidden** anywhere in the output — body text, figure captions, footnotes, and section titles alike. Describe the physics directly ("The trajectory is sketched in Fig. 2"), not its provenance.
7. **One output document per input document.** Each source PDF is a distinct topic and gets its **own** end-to-end chain and its **own** final `.tex` + compiled PDF. Three input PDFs covering three topics produce three output documents — never one merged document, never a split of one input across several. The mapping is strictly 1:1.
8. **Figures are the source images themselves.** Every figure in the final document is a **high-fidelity image crop of the source drawing** — never a TikZ/vector redrawing, never a substitute diagram, never an omission. Each figure's **caption states the intention of the original drawing**: what the diagram is showing and why it matters at that point in the physics (axes, labeled quantities, limits, geometry). Per Principle 6, the caption describes the physics directly and never mentions notes, boards, or the source medium.
9. **Accessible by construction, not by retrofit.** The output PDF must be **tagged**: a real structure tree (headings, paragraphs, lists, figures), an explicit reading order, alt text on every image, a declared document language, and math that carries semantics rather than positioned glyphs. Accessibility is designed into the build (Stage 4) and captured during segmentation (Stage 1) — it is never bolted on after the fact. An untagged PDF is a **failed run**, however good the physics is.
10. **Verify accessibility with a tool — and do not trust the tool, including this pipeline's own checkers.** No agent may report a document as accessible on the strength of its own reading; conformance is established by running a checker (veraPDF, PAC, Acrobat) and preserving the report. But **a conformance pass is a floor, not evidence.** veraPDF can return a clean pass in three consecutive audits while a document still has 16 headings mis-tagged as paragraphs, 24 content operators orphaned outside the tag tree, a table cell artifacted so that "Quantum" vanishes and inverts the sense of a comparison, and every figure announced after the final section under an unrelated chapter. This pipeline's *own* `check_structure.py` can report `mathml_empty: 0` while eight equations carry only a replacement character — and even after that specific bug is fixed, it can still pass by comparing *counts* of spoken fallbacks to empty shells and hard-coding a string like "(all boxed)", so an empty `\xcancel` with no fallback and a spoken ovaleq that is *not* empty cancel each other out in the tally. A checker can just as easily claim table `/Summary` "3 of 3" while the attribute actually sits on the first `TH`, or "20 U+FFFD all in boxed shells" while twelve of them do not. **A checker that cannot fail, or that tests a proxy instead of the claim, is not a check.** The tests that actually catch these are in Step 4d and are **mandatory in addition to** veraPDF. Where the pipeline falls short, the gap is **stated explicitly** in the run log rather than glossed over. Logs, the manifest, the auditor report and the hand-off report must match an independent measurement of the frozen PDF; a false claim in those artifacts is itself a REVISE (Stage 4c, adversarial referee).
11. **Some criteria can only be checked by a human-equivalent judgment — budget for them.** Acrobat's own report marks **logical reading order** and **color contrast** as *"needs manual check"* and **table summary** as *skipped*; no tool will ever return a verdict on these. They are not exempt because they are unautomatable — they are the ones most likely to be quietly skipped, so the Accessibility Auditor must render an explicit written verdict on each, with the evidence it used (a reading-order walk, a measured contrast ratio), and the run log must show that verdict. "Needs manual check" appearing unresolved in a shipped report is a failed run.
12. **Prefer the format that carries structure natively.** Where an institution's guidance is to reduce PDFs and choose a native format (Canvas page, Word, web page) where possible — Ohio University's is, see the institutional profile in the Governing Standard section — this pipeline must still produce the tagged PDF because that is the requested deliverable, but the HTML + MathML companion is the artifact that best matches that preference, and Stage 5 must present it as such rather than burying it as a by-product. A pipeline that only ever emits PDFs is answering a narrower question than the one most institutions are actually asking.

---

## Toolchain Prerequisites

**Check this before Stage 0. Getting it wrong invalidates the whole run, and the failure is silent.**

- **A LaTeX kernel from 2024 or later is mandatory.** Earlier kernels cannot tag mathematics at all. The TeX Live shipped by Debian/Ubuntu (2022 at time of writing) is *not* sufficient: `\DocumentMetadata` either errors or accepts module names it then ignores with only a warning, and you get an untagged-math PDF that still passes veraPDF.
- **`pdflatex` can never be used.** It predates PDF structure tags; every PDF it produces is untagged regardless of the source.
- Required: **LuaLaTeX** from TeX Live 2024+, plus `unicode-math`, `float`, `accsupp`, and a conformance checker (**veraPDF**, free and scriptable). Also **poppler** (`pdftoppm`) and python3 with `pymupdf`, `pillow`, `numpy`.
- **The page rasteriser is part of the measurement, so pin it.** Seam rows, `content_bounds`, and every figure crop box are pixel coordinates in one particular raster. Poppler and PyMuPDF differ in antialiasing and, on US Letter at 300 dpi, in page height (3301 rows against 3300) — re-render with the other engine and every recorded box shifts underneath you. `render_pages.py` prefers `pdftoppm`, which is what the worked example in `Example_Deliverable_Directory/` used, and writes the engine into `render.json`. If a manifest was measured under one engine and the pages were re-rendered under the other, re-measure; do not reuse the boxes.
- **Probe the toolchain, do not assume it.** Compile a three-line document containing one equation, one list, one table and one figure, then check the produced PDF for `/Formula`, `/L`, `/Table`, `/TH` and `/Alt`. If any is absent, stop and fix the toolchain — do not start the pipeline. Silent degradation is the normal failure mode here: unknown `testphase` modules and the ignored `alt` key both warn at most. **Inspect the output PDF, not the log.** `TH` is reachable in this kernel through `table/header-rows`; claiming it from the preamble without opening the file is exactly how a build can silently ship zero header cells despite the preamble looking correct.
- **MathML needs at least three LuaLaTeX passes.** luamml writes fragments on one pass and embeds them on a later one; a two-pass build ships `/Formula` elements with no mathematics attached. The production compile is always three passes.

```latex
% probe preamble — the modules this pipeline depends on
\DocumentMetadata{lang=en-US, pdfstandard=ua-1, pdfversion=1.7,
  testphase={latest,math,table,sec,title,float,graphic}}
```

**Target UA-1, not UA-2, unless you have a specific reason not to.** Both are real, kernel-supported targets (`g__pdfmeta_standard_pdf/UA-1_prop` / `UA-2_prop` in `latex-lab`'s own `pdfmanagement.ltx`) — this is a declared-standard choice, not a toolchain limitation either way. UA-2's `/AF`-only math tagging looks more capable on paper, but **the checker most institutions actually run still checks against UA-1** (Ohio University's PAC 2026 does, per this kit's institutional profile — see Governing Standard), and UA-1's clause 7.7 does not recognize `/AF` as alternative text at all: a document that declares UA-2 will show every Formula lacking `\formulaalt` as missing alt text, no matter how clean its other tagging is. Declaring UA-1 instead flips a real kernel behavior (`latex-lab-math.ltx`, `math/alt/use`): on UA-1 detection it auto-writes `/Alt` on every Formula (the raw LaTeX source, not spoken math — lower quality than a hand-authored `\formulaalt`, but non-empty and conformant), closing that gap for every formula that doesn't already have a better hand-authored alternative. Verified on the worked example in `Example_Deliverable_Directory/`: declaring UA-1 flips veraPDF UA-1 from FAIL to PASS, all 198 Formulas go from 9/198 to 198/198 carrying alt text or ActualText, with 0 recovered TeX errors across 3 passes and no other Step 4d test regressed. **Consequence to plan around:** UA-1 caps at `pdfversion=1.7` (`min_pdf_version=1.4, max_pdf_version=1.7` in the kernel's own standard table) — you cannot declare both UA-1 and PDF 2.0. Run both `verapdf -f ua1` and `-f ua2` regardless of which is declared (Step 4d); the un-declared one failing is expected and informative, not a defect.

---

## Agents

| Agent | Role |
|-------|------|
| **Prime Agent** (orchestrator) | Runs the pipeline end to end: ingests input PDFs, performs segmentation, submits work for review, applies feedback, assembles final outputs. |
| **Reviewer Agents ×3** (physics-PhD-level experts) | Independently inspect the segmented PNG outputs for legibility, correct segmentation, and faithful capture of the physics/math content. Each returns explicit feedback and an APPROVE / REVISE verdict. |
| **Final Review Agents ×5** (physics-PhD-level experts) | Independently inspect **each** compiled LaTeX PDF from Stage 4 for correctness, legibility, and fidelity to the source. They also act as journal/publisher referees: they heavily scrutinize whether the document follows the notation conventions of the reference textbook chosen in Stage 4 and whether its typesetting is **publication-ready by a major physics publisher's standard** — while confirming the content is drawn from the source with only sparse, very concise additions, contains **no reference to notes/boards/lectures/pages**, and opens directly with the content, with no agent/pipeline introduction. Assign emphases so the five do not duplicate: coverage and restraint · physics · typesetting · figures/captions/alt text · **adversarial (claims vs artifacts)**. Each returns abundant, scrutinized feedback until all five approve. |
| **Accessibility Auditor ×1** (document-accessibility specialist) | Owns Principles 9–12. Audits **each** compiled PDF against PDF/UA and WCAG 2.1 AA as adopted by the receiving institution (Ohio University in this kit's institutional profile — see Governing Standard). Runs the conformance checker **and** the four numeric tests in Step 4d — element inventory, MCID reachability, artifact audit, figure reading position — plus a MathML content check, the Acrobat rule-map sweep, the MDAS five, and a screen-reader walk. Issues an explicit written verdict on the three items no tool decides (reading order, color contrast, table summary) rather than passing the "needs manual check" label through. Must **measure and report numbers**, never repeat a stored report or accept a checker pass as proof. Holds an independent **APPROVE / REVISE** vote that no physics reviewer can override; a visually flawless but structurally broken document is an automatic REVISE. Expect this agent to be the last one still saying REVISE. |

---

## Pipeline Stages

### Stage 0 — Ingest
Feed the handwritten / board-written PDF files into the framework.

- **Input:** one or more source PDFs (handwritten pages, whiteboard/chalkboard photos). Multiple inputs may be submitted in a single run and processed in parallel.
- **Pre-flight:** if working directories from a previous job exist, archive them (timestamped `Run_Archive/` folder) before starting, so the new run begins clean.
- **Action:** register the files, verify they are readable, and stage them for segmentation. Assign each input to its own subagent chain so independent inputs move through the pipeline concurrently.
- **One chain per input.** Give each source PDF a short topic slug (e.g. `oscillations`, `rotations`, `scattering`) derived from its subject matter, and carry that slug through every stage: its own segment directory, its own assembled PDF, its own `.tex`, its own compiled PDF. Inputs are **never merged** into a shared document, and a single input is **never split** across multiple documents.
- **Manifest:** the Prime Agent records the input → slug → output-document mapping up front and verifies at the end that the count of final PDFs equals the count of input PDFs.

### Stage 1 — Segment to PNG
Create (or invoke) a **segmentation skill/extension** that splits each page into legible, readable PNG files.

- **Rasterise the pages first, once, at a recorded dpi** (`render_pages.py`, 300 dpi floor). Everything after this works on the page rasters rather than the PDF, and every seam row and crop box is a coordinate in them — so the render is the coordinate system the whole stage is measured in. Re-rendering later with a different engine or dpi invalidates the manifest. A figure that needs more resolution gets its own higher-dpi render of that page rather than an upscale of this one.
- Segment by logical unit (equation block, diagram, paragraph of notes) so each PNG is independently readable.
- **Overlap is allowed and encouraged** where it improves readability — adjacent segments may share content rather than cutting a figure or equation in half.
- **Diagram segments double as final figures.** Any segment containing a drawing/diagram must be cropped cleanly around the drawing (including its labels and axes) at **high resolution**, because that same PNG will be embedded as the figure in the final LaTeX document (Operating Principle 8). Do not let a diagram straddle a segment boundary or come out blurry, skewed, or clipped.
- **Draft alt text at crop time.** Every diagram segment gets an **alt-text description written while the drawing is being looked at** — this is the cheapest and most accurate moment to write it, and it is what makes the final figure accessible (Principle 9). Store it in an `alt_text.json` sidecar keyed by **final figure filename**, so the descriptions can be reviewed on their own and the build can fail hard when one is missing. Stage 4b reads that sidecar; the physics and the accessibility metadata never get entangled in the same file.
  - Alt text describes **what the drawing shows**: the geometry, the labeled quantities, the axes, the limiting behavior a curve illustrates. One to three sentences — enough that a reader who cannot see the figure can follow the adjacent derivation.
  - It is **not** the caption repeated. The caption states the figure's role in the physics; the alt text states its visual content. A figure needs both, and they should not be identical strings.
  - Provenance language is banned here exactly as in body text (Principle 6): describe the geometry, never "the sketch on the page."
- **Check contrast at crop time, because a figure crop is the one piece of the deliverable that stays an image.** Everything else in the output becomes real text whose contrast the LaTeX build controls; the diagram crops inherit whatever contrast the original pencil-on-paper or chalk-on-slate had, and light pencil on cream paper routinely lands well under the WCAG 1.4.11 non-text-contrast threshold of **3:1**. Measure the ink-versus-background ratio on each diagram crop and, where it falls short, raise it (levels/threshold adjustment on the crop, never a redrawing — Principle 8 still holds) and record the before/after ratio in `segment_manifest.json`. A crop nobody with low vision can resolve is not saved by having good alt text; it needs both.
- **Never encode information by color alone** (WCAG 1.4.1). If the source distinguishes two curves only by ink color, the caption and alt text must name the distinguishing feature in words. Record any such case in the review log so Stage 4c reviewers see it.
- **The ink mask must see every pen, including saturated colour.** A rule that keys on "dark and not much bluer than red" discards blue pen *and* red strike-through. A darkness cap (`max(RGB) < 235`) then misses saturated red entirely — it can see as little as 0.2%, then only 2.1%, of an 11,405-pixel retraction mark that should register as fully covered. The discriminator on these pages is GREEN: printed ruling is cyan (G−R ≈ +95), violet pen is not (G−R ≈ +12). Keep anything dark **or** strongly coloured, and reject only the ruling. Verify the mask against a known coloured mark (pixel count in, pixel count out) before trusting coverage or seams. Fixing the mask can move seams; re-measure `content_bounds` after the fix.
- **Crop boxes are measured against the drawing, not against a nearby heading.** Extending a crop to "include the whole band" will import an adjacent equation line if that line's ink is in the same column. Record the box in `figure_crops.json` as the measured rectangle, and fail a crop that slices a word or that contains a body-text display the caption does not own.
- **Output:** a set of PNG files per source page, with a naming scheme that preserves page order and segment order (e.g. `page03_seg02.png`), plus a `segment_manifest.json` recording every segment's page and pixel bounds, and an `alt_text.json` sidecar.
- **The manifest is the authoritative inventory — never infer the segment list.** Segment counts differ per page (a run may yield 4/3/4/4, not 4-per-page), and any agent or script that assumes a uniform naming range will silently skip or invent files. Every downstream stage reads `segment_manifest.json` and works from what is actually there.
- **Prove no ink was cut away before the reviewers see the segments** (`check_coverage.py`): every ink row inside a page's content band must fall inside at least one segment span. This gate exits non-zero and names the uncovered row ranges. It is cheap and it catches the one defect a reviewer reading segment images cannot — content that is in no image at all, and so is invisible to anyone looking only at what was produced.

### Stage 2 — Expert Review Loop
The Prime Agent's PNG output is scrutinized by the **3 physics-PhD-level reviewer agents**.

- Each reviewer examines every PNG for legibility, segmentation quality, and content fidelity, and returns concrete feedback.
- Reviewers must be PhD-level physics experts and act as heavily strict, serious critics — scrutinizing the segmentation, the underlying physics, and the logic of the material.
- Reviewers also check that segment overlap is used correctly: enough overlap to avoid losing information at segment boundaries, without being excessive.
- **Reviewers also read the drafted alt text.** For each diagram segment, a reviewer confirms the alt text accurately describes the drawing's geometry and labeled quantities, is specific rather than generic ("a graph" or "a diagram of the system" is a REVISE), and carries no provenance language. Alt text that a blind reader could not use to follow the derivation fails this check. Reviewers also confirm the recorded contrast ratio for each diagram crop clears 3:1, and that any adjustment preserved the original drawing rather than redrawing it.
- **Every round must re-check the previous round's fixes for regressions.** A fix is as likely to break something as the original defect was. A round-1 fix that re-splits an over-stuffed segment can put the new seam straight through a diagram the previous seam left untouched — exactly the kind of regression round 2 exists to catch. Each round's brief therefore states what was changed and asks reviewers to verify those changes specifically, not just to look for new problems.
- **Measure; do not estimate.** When reviewers disagree on a boundary, settle it with the pixels rather than by averaging opinions. Three reviewers proposed three different seams (1995 / 2000 / 2010); a row-wise ink profile of the page showed the figure band quiet through y2000 and the next heading rising sharply at y2005, which decided it. The same measurement corrected an automated estimate that had counted 1-pixel-per-row grid noise as content.
- **Loop condition:** Stages 1 ↔ 2 repeat — the Prime Agent re-segments per the feedback — until **all reviewers approve**. Only then does the pipeline advance. Expect roughly three rounds; a first-round approval usually means the reviewers were not strict enough.
- Keep a short log of each review round (round number, feedback given, changes made) so the loop is auditable. **A round that returned APPROVE ×3 is not closed until those three verdicts are written into the log.** Success Criterion 3 is the log, not the agents' chat. A round can return APPROVE ×3 with the log still reading "verdicts: see below" — an adversarial referee must treat that placeholder as an open criterion, not a closed one.

### Stage 3 — Assemble Reviewed PDF
Paste the approved PNGs, in order, into a compiled PDF — **one per input document**.

- **Output:** for each source PDF, one assembled PDF containing that input's approved segments in reading order. Assembled PDFs from different inputs are never combined.

### Stage 4 — Direct LaTeX Compilation (Tagged / Accessible)
Take the final PDF / pictures and produce a **LaTeX-compiled, tagged PDF** directly.

**Step 4a — Choose the reference textbook convention (before writing any LaTeX):**

- The Prime Agent first identifies the standard physics textbook(s) whose subject matter **best matches the content of the class notes** (e.g., Griffiths for E&M or QM, Taylor for classical mechanics, Jackson for graduate E&M, Sakurai for graduate QM, Kittel/Ashcroft & Mermin for solid state).
- **The textbook serves two purposes only:** (1) **context** — it helps the agents learn and understand the material in the notes; and (2) **notation conventions** — it fixes the symbols, vector/tensor notation, unit system (SI vs. Gaussian), and equation-formatting style used when transcribing. It is **not** a license to rewrite the notes in the textbook's voice or structure — the content itself stays faithful to the original notes.
- This choice must itself be **heavily scrutinized**: the Prime Agent must state which textbook(s) it chose, why they best match the notes, and the reviewer agents must challenge that choice before transcription begins.

**Step 4b — Transcribe and compile in that convention:**

- **The build must emit a tagged PDF.** This is an engine-and-preamble decision made *before* transcription. Required setup:
  - Compile with **LuaLaTeX** (TeX Live 2024+), opening the file with the document-metadata declaration *before* `\documentclass`:
    ```latex
    \DocumentMetadata{
      lang        = en-US,
      pdfversion  = 1.7,
      pdfstandard = ua-1,
      testphase   = {latest,math,table,sec,title,float,graphic},
    }
    \documentclass[11pt]{article}
    ```
    The `testphase` list is **module-based**, not a single phase name. Naming a module the installation does not have produces a warning and is then ignored — the build succeeds and the feature is silently absent. Verify the modules landed by inspecting the output (Step 4d), not the log.
    **`pdfstandard = ua-1` (not `ua-2`) — see the Toolchain Prerequisites note above for the full reasoning.** In short: PAC 2026 checks UA-1, UA-2's `/AF`-only math tagging fails UA-1's clause 7.7 on every Formula without a hand-authored `\formulaalt`, and declaring UA-1 instead makes the kernel auto-write `/Alt` on every Formula (raw LaTeX source — real but lower-quality than `\formulaalt`, disclose it as such). `pdfversion` must be `1.7` or lower with `ua-1` — the kernel enforces `min 1.4 / max 1.7` for that standard and will not let you combine `ua-1` with `pdfversion=2.0`.
  - This gives structure tags for sections, paragraphs, lists, tables, links and footnotes; reading order; MathML on equations; and the PDF/UA identifier. Sectioning must use real `\section`/`\subsection` commands — hand-formatted bold-and-bigger pseudo-headings produce no tags and are forbidden.
  - Set a real document `\title` and language, and use `\maketitle`; both land in the PDF metadata a screen reader announces.
  - **Set math in an OpenType font** (`\usepackage{unicode-math}` + `\setmathfont{Latin Modern Math}`). Computer Modern's math fonts carry **no ToUnicode map**, so without this every symbol in every equation is unextractable and fails conformance outright. This is a correctness requirement, not a typographic preference.
  - Keep the shared style file tagging-clean: no raw `\hbox`/`\vbox` wrappers around body text, and **no legacy glyph hacks**. `\mathchar'26` and similar address slots in the old Computer Modern encoding and produce *nothing* under `unicode-math` — this silently erases the bar from the inexact differential, so `đQ + đW` prints as ordinary exact differentials with no warning. Use the real Unicode character instead.
- **Pin every figure with `[H]`; never let a figure float.** A LaTeX float is typeset where the page builder chooses, but its *structure element is appended to the tag tree at the very end of the document*. An unpinned figure can end up appended at the very end of the tag tree regardless of where it sits on the page — e.g. every figure and caption in a document landing in its final handful of reading positions, announced after the last section, under an unrelated final heading, with nothing tying them to the text they illustrate (WCAG 1.3.2). Load `float` and write `\begin{figure}[H]`. Do **not** "fix" this by replacing the float with `center` + `\captionof`: that corrects the ordering but breaks conformance, because a `Caption` must remain a child of its `Figure`.
- **Boxed display math needs an `/ActualText` fallback on the Formula element itself.** `\boxed` hands the math tagger an opaque box and the boxed expression exports as MathML containing no equation; `\fbox`, `\ovalbox`, `tcolorbox` and `\xcancel` over mathematics all behave the same way. Where the source boxes (or strikes) a result, keep the mark (Principle 4) and attach a spoken rendition **as `/ActualText` on that Formula**. Do **not** wrap an extra `accsupp` span *inside* the Formula: the inner span plus the Formula plus the content-stream fallback is what causes a boxed equation to be announced multiple times by a screen reader. The style file's `\formulaalt` writes the spoken string onto the current Formula via the tag-structure property table; `\boxeq`/`\ovaleq` call that and nothing else.
  Write the fallback as a reader would say it aloud ("sigma of theta equals one quarter times, Z Z prime e squared over 2 E, all squared, times cosecant to the fourth power of theta over 2"). The run log records which equations rely on it, **identity-matched** (this Formula, this `/AF`, this `/ActualText`) — never by comparing counts of spoken strings to counts of empty shells, and never with a hard-coded "(all boxed)". Ovaleq can be spoken and still not empty; `\xcancel` can be empty and still not boxed.
- **Never nest a figure or graphic inside a `\[...\]` display.** It breaks the tagging context and orphans the surrounding content — it can orphan dozens of content operators, including a symbol definition referenced two paragraphs later. Give the graphic its own `figure` environment.
- **Math markup should be semantic.** Use `\frac`, `\sqrt`, `\vec` and proper `\text{}` for words inside math rather than visually-faked spacing; the tagger can only export meaning the markup actually encodes. Give every display equation the body cross-references a real number/label.
- **Lists must be real list environments.** Use `itemize`/`enumerate`/`description`; never fake a list with `\item`-less line breaks, dashes at the start of a line, or an aligned two-column layout. The tagger emits `L → LI → Lbl + LBody` only from a real environment, and Acrobat's *"Lbl and LBody must be children of LI"* rule fails on hand-built imitations. Nested lists must nest as environments, not by indentation.
- **Tables need a real header row, a summary on the Table element, and a caption–rule gap that is actually there.** Any `tabular` carrying data must mark its header row so the tagger emits `TH` rather than a row of `TD`. Give each table a one-sentence `/Summary` of what it compares (Acrobat reports a missing summary as *skipped*, which is a silent omission, not a pass). **The `/Summary` must sit on the `Table` element, not on the first `TH`** — and it must sit **inside `/A` with `/O /Table`**, not as a bare top-level key on the `StructElem` dict. This kernel's own tag-property API (`__tag_struct_prop_gput:nnn`) writes whatever key you give it directly onto the `StructElem`, which is how `\tablesummary` first shipped, and a bare `/Summary` there is simply not a key ISO 32000 defines — it satisfies nothing per spec, even though `check_structure.py` reported it as present for months because that test only checked for the string anywhere on the element. **PAC 2026 flags this as 3/3 Tables "possibly inappropriate use" with no attribute-level cause visible until the `/A` location is checked directly**, and it is closed post-build by `tools/fix_pdf_tagging_defaults.py`, which promotes the existing text into a proper `/A << /O /Table /Summary (...) >>`, additive alongside the legacy key rather than removing it. `check_structure.py`'s own test must check the `/A` location specifically (`tables_summary_not_in_A`), not just presence anywhere on the element — verify it actually fails against an old, unpromoted build before trusting it to pass a promoted one. Place the summary command in `\noalign{...}` immediately after `\begin{tabular}` so it does not start a cell; walk the tag-structure stack for a Table/tabular ancestor rather than assuming the current ID is the table. Do not use the predicate form `\tl_if_in_p:Nn` for that walk — it is not defined for `\tl_if_in:Nn` and recovers as 40 errors per table; use `\tl_if_in:NnTF`. Tagged captions **ignore** `\captionsetup{skip=...}`; the gap a reader sees is `\abovetopsep` inside the tabular. Measure caption-ink bottom to `\toprule` at 300 dpi and keep it ≥ 6 pt so the rule does not underline descenders. Never use a table for visual layout — if it is not data, it is not a table. Header cells in this kernel take `/Scope` through `/C /TH-col` and the ClassMap (`/TH-col << /O /Table /Scope /Column >>`); looking for a direct `/Scope` key and reporting "none" is a false negative — the same class of gap as the `/Summary` placement above, both closed the same way (promote into a direct `/A`, post-build).
- **Link text must describe its destination** (WCAG 2.4.4). "See the derivation in Sec. 3" is a link; "click here" and a bare URL are not. If a URL must be visible in print, put the descriptive text in the link and the URL in a footnote. Every link annotation also needs `/Contents` — the UA-1 profile checks this and UA-2 does not, which is why Step 4d runs both.
- **Emit PDF bookmarks and check the tab order.** Load `bookmark` (or let `hyperref` build the outline) so the document has a navigable outline matching its heading structure — Acrobat's *Bookmarks* rule expects them in any document of length, and for a notes document the outline is the primary way a screen-reader user moves around. Tab order must follow structure order (`\hypersetup{pdfpagemode=UseOutlines}` plus tagged structure gives this by default; verify it rather than assuming).
- **Colors must clear contrast thresholds in the built PDF, not just in the source crops.** Body text and any colored link text need **4.5:1** against the page (WCAG 1.4.3); rules, borders and other non-text indicators need **3:1** (1.4.11). `hyperref`'s default link colors do not reliably clear 4.5:1 on white — set them explicitly (`\hypersetup{colorlinks=true, linkcolor=..., urlcolor=...}` with measured values) or use black text with an underline. Never carry meaning by color alone.
- **Leave the accessibility permission flag set and add nothing that flashes.** Do not apply PDF encryption or permission restrictions that block content extraction — that single flag is MDAS item 1 and it disables assistive technology outright. No animated, blinking, or auto-updating content (WCAG 2.3.1, and Acrobat's *Screen flicker* rule); for a static notes document this is free, but it must be confirmed rather than assumed.
- **Character encoding is the rule this toolchain actually fails.** Acrobat's *"Reliable character encoding is provided"* check is what catches a font with no `ToUnicode` map, and it is the concrete failure mode behind the `unicode-math` requirement above. Test it the way it will be tested: extract the text of an equation-dense page and read it back. If symbols come out as `�`, boxes, or private-use codepoints, the encoding is broken no matter what the visual output looks like.
- **Ship an HTML + MathML companion alongside the PDF**, built with `make4ht` (or LaTeXML). It reflows, its MathML support is the most mature of any route, and it is the fallback wherever the PDF's math tagging falls short — boxed results above all. The PDF remains the primary deliverable; the HTML is a required sibling.
  - `make4ht` writes `alt="PIC"` for **every** `\includegraphics` and rasterises any math it cannot convert, giving those images alt attributes full of leaked markup. A post-processing pass must rewrite figure alt text from the sidecar and report how many equations were rasterised — that count is the honest measure of what the HTML route failed to make accessible.
- **One `.tex` per input document.** Each source PDF is transcribed into its own `.tex` file and compiled to its own PDF, named with that input's topic slug. Do not merge topics into a combined document.
- Transcribe the approved content into a `.tex` document using the chosen textbook's **notation conventions**, keeping the material **as close to the original notes as possible**. Do not restructure, expand, or rewrite the notes into textbook prose.
- **The body is the source content.** Transcribe what is actually there — every equation, intermediate step, diagram, label, and marginal remark. Do not drop steps because they seem obvious, and do not import textbook material the source does not cover.
- **Figures = embedded source images.** Every diagram in the source appears in the `.tex` as an `\includegraphics` of its **high-fidelity PNG crop** from Stage 1 (cleaned/straightened as needed, but the original drawing itself — never redrawn in TikZ or replaced with a lookalike). Each figure gets a numbered caption that **conveys the intention of the original drawing** — what physical setup, quantity, or limiting behavior it illustrates and how it connects to the adjacent derivation — written in the document's own voice with no provenance language (Principles 6 and 8). Body text cross-references the figure by number ("see Fig. 3").
- **Every figure carries alt text.** Each `\includegraphics` takes the description from `alt_text.json`, passed through the `alt` key: `\includegraphics[alt={...}, width=...]{page03_seg02.png}`. An image with no `alt` is announced as an unlabeled graphic or skipped outright, which here means losing the physics entirely — so a missing or empty `alt` is a **build failure**, enforced by the build script, not a warning. Decorative rules or spacers are marked artifacts so the reader skips them rather than reading noise.
- **Transcribe source errors as written and flag them; never silently repair them, and never silently propagate them.** Both failure modes are real, and both are the kind final review catches rather than an earlier gate: an unflagged transcription slip (`f(x,y) = u\,dx + v\,dy`, where `df` was meant) can ship silently, and a genuine source error (a missing `dt`) can just as easily be quietly "corrected" by the transcriber instead of flagged. The rule is a single consistent policy — reproduce the source, then flag the discrepancy in a short bracketed editorial remark placed after the display it concerns. Apply it to every erratum in the document or to none. **Do not insert the device in the middle of a sentence** — that leaves orphan fragments ("this becomes", "and substituting into Eq. (9),") as their own paragraphs. If the handling *changes* the source (casing, literal markup set as mathematics), do not also claim "Reproduced above as written"; use a star form of the device that omits that sentence. A false erratum is as damaging as a missed one: withdraw it, do not leave it flagged.
- **Additions are the exception, not the rule.** Add a clarifying line only when a step is otherwise unfollowable (e.g. an unstated substitution or an undefined symbol). When you do, keep it to a clause or one short sentence, in the same notation, and place it adjacent to the step it serves. Prefer a shorter addition over a longer one; prefer no addition over a short one. A reader should not be able to tell added lines from transcribed ones by their length or tone.
- **Never reference the source medium.** The prose must not mention notes, boards, lectures, pages, scans, or handwriting — see Operating Principle 6. Write about the physics directly. Cross-references point to the document's own numbered equations and figures ("substituting into Eq. (12)", "see Fig. 3"), never to the source material or to its physical layout ("the box at the bottom of the page", "the sketch on the right").
- The document must **start directly with the notes content** — no introduction describing what the agents did, how the pipeline works, or how the document was produced.
- Compile it **three times** with LuaLaTeX and confirm it builds cleanly (no errors, no unresolved references, no overfull-box sloppiness in the final PDF). Tagging warnings count as errors for this purpose — an untagged-content warning means a passage is missing from the structure tree. Recovered TeX errors in the log (even if the PDF looks fine) are recorded in the run log; they are not "zero errors."
- **Self-check before review:** grep the `.tex` for banned provenance wording (`original notes`, `the notes`, `on the board`, `blackboard`, `whiteboard`, `handwritten`, `the lecture`, `the lecturer`, `as shown above in the`, `the page`, `the scan`) and rewrite every hit before handing off to the reviewers.
- **Accessibility self-check before review:** confirm `\DocumentMetadata` is present with a language set; every `\includegraphics` has a non-empty `alt`; every `figure` uses `[H]`; no section heading was faked with manual formatting; every boxed or struck display has Formula-level `/ActualText` (boxes stay — they just cannot be silent); every list is a real list environment; every data table has a marked header row and a `/Summary` on the Table; every link has descriptive text; bookmarks were generated; link colors were measured against 4.5:1; no permission restrictions were applied; and the HTML companion built. Then run the Step 4d structural tests yourself. Fix all hits before the review agents are spawned — do not spend reviewer rounds on defects a script would have caught.

**Step 4c — Publication-readiness review:**

- Once compiled, **5 physics-PhD-level agents** heavily scrutinize the result and give abundant, rigorous feedback. **Freeze the PDF (record its MD5) for the duration of the round** and give every referee that hash; a rebuild landing underneath a review is a failed round.
- The evaluation bar is explicit and strict: the final product must be judged **publication-ready by the standard of a major physics publisher** (e.g., Springer, Cambridge University Press, Pearson, APS journals) **in typesetting quality** — typography, notation consistency, and physical correctness — while the **content remains a faithful rendering of the original notes**, not a textbook rewrite.
- Each reviewer must explicitly verify and report on **all seven**:
  1. **Coverage and fidelity** — the document tracks the source closely: nothing in the source is missing, and nothing is restructured or rewritten into textbook prose.
  2. **Restraint in additions** — any material not in the source is genuinely necessary and very concise. A reviewer who finds padding, generic textbook exposition, or an added paragraph where a clause would do must call it out and issue REVISE.
  3. **No provenance language** — the document nowhere refers to notes, boards, lectures, pages, scans, or handwriting. Reviewers scan the text (including captions and footnotes) for this and treat **any** occurrence as an automatic REVISE.
  4. **Convention and typesetting** — adherence to the reference textbook's notation conventions and publisher-grade typesetting quality.
  5. **No meta-introduction** — the document opens directly with the content, with nothing about the agents or the pipeline.
  6. **Figure fidelity and captions** — every source diagram is present as a **high-fidelity image crop of the original drawing** (legible, unclipped, not redrawn or substituted), and every caption accurately conveys the intention of that drawing — what it illustrates and its role in the derivation — without provenance language. A redrawn figure, an illegible crop, or a caption that misstates or ignores the drawing's purpose is an automatic REVISE.
  7. **Accessibility** — the PDF is tagged, every figure has meaningful alt text distinct from its caption, headings are real sectioning commands, lists and tables use real structures, link text is descriptive, the document language is declared, and the HTML/MathML companion exists. Reviewers walk the **7 Core Skills** table in the Governing Standard section and confirm each row is satisfied or explicitly marked not-applicable. They confirm the Accessibility Auditor's report is attached and passing; a document that is publication-ready visually but untagged is an automatic REVISE (Principle 9).
- **One of the five is adversarial.** That referee's job is the gap between what the artifacts claim and what the frozen PDF measures. A log, manifest, auditor report or hand-off report that states a number the PDF does not support is a REVISE even if the PDF itself is fine. Known-partial items are allowed only when the disclosure matches the measurement.
- Reviewers evaluate **each output document separately** and also confirm the 1:1 mapping: one final PDF per input PDF, with no topics merged and none split.
- **Loop condition:** if any expert requests changes, the pipeline is re-run from the appropriate earlier stage until **all 5 experts agree** the compiled PDF is correct **and publication-ready** — and the **Accessibility Auditor** independently approves. All six approvals are required; a physics reviewer cannot waive the accessibility verdict, and the auditor cannot waive the physics verdicts.
- Between rounds, the Prime Agent revises by re-reading the original notes and consulting the web or its training data on the underlying physics — to better understand the content and resolve the experts' feedback before the next review pass.
- Place the `.tex` source and compiled PDF into **`Final_Product_Ready/`** (create it if it does not exist).

**Step 4d — Accessibility verification (tool-based, per document):**

Run by the Accessibility Auditor on every compiled PDF. No document leaves the pipeline without a stored report.

- **Machine check.** Run **veraPDF** against the standard the document declares (`-f ua1` — see Step 4b). Save the report to `Final_Product_Ready/accessibility/`. Running **both** `ua1` and `ua2` is worthwhile: where they disagree, the disagreement is informative — a link annotation with no `/Contents` was once found this way, and declaring `ua1` will now correctly show `ua2` failing on `pdfversion` alone (expected, not a defect, since `ua1` caps at PDF 1.7).
- **Institutional check.** Run whatever tool your receiving institution names as its own reviewer's checker (see Governing Standard → your institution's profile) and store its report — its verdict is the one that will get quoted back to you, so a passing veraPDF run is not a substitute. **Worked example — Ohio University names PAC 2026** (PDF Accessibility Checker, Windows only, free software from axes4 GmbH, distributed for convenience through OHIO's Company Portal but not gated behind it — the same installer is public: `winget install axes4.PAC`, or the direct download at pac.pdf-accessibility.org). Do not treat "Windows-only" as "unrunnable from here" and skip this step: **if this agent is running inside WSL, check for a Windows host before writing PAC off** — `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "winget install --id axes4.PAC --exact --silent --accept-package-agreements --accept-source-agreements"` installs it silently (or confirms it is already installed) on the host Windows machine one `cd` away. **PAC has no CLI or batch mode** (confirmed by search, not assumed) — `axesSense` is axes4's separate automation product and is not part of a standard PAC install. So this step cannot be fully scripted: after installing, launch it pointed at the built PDF (`Start-Process` with the PAC exe, found via `Get-StartApps | Where Name -match PAC`, and the PDF path translated with `wslpath -w`) so it is one click away, then the operator runs the check and exports PAC's report themselves — record that report in `Final_Product_Ready/accessibility/` exactly like the veraPDF ones. Where no institutional checker can be run at all (no Windows host reachable, or the receiving institution names none), say so plainly in the report; do not let a veraPDF pass stand in silently for it. If Acrobat Pro is available, generate its accessibility report with **all** rule categories enabled (not a narrower subset scoped to one submission type) and **attach the report to the PDF** — this is good practice regardless of institution, and it happens to match Ohio University's own ETD convention.
- **Institutional floor checklist.** Confirm your receiving institution's minimum checklist item by item and record each. **Worked example — Ohio University's MDAS**: permission flag set; title present; full text present (not image-only); text language specified; alt text on every figure. All five are necessary and none is sufficient; if your institution names a different or longer list, use that one instead.
- **A checker pass proves almost nothing on its own.** Every defect below passed veraPDF cleanly. The following four tests are **mandatory acceptance criteria**, and each has a numeric answer that must be recorded:
  1. **Structure-element inventory.** Count each element type. Compare heading counts against the source: *n* `\section` + *m* `\subsection` must produce exactly that many H-elements, correctly nested with no skipped levels. Headings can silently tag as ordinary paragraphs across an entire document — e.g. all 16 headings collapsing to plain paragraphs, leaving one real heading and no navigable outline — while the checker passes regardless. **Acceptance: headings 1:1 with the outline.**
  2. **Content reachability (MCID walk).** For every text-showing operator, determine whether it is inside `/Artifact`, reachable from the structure tree via an MCID the tree actually references, or neither. Note that content may be marked with `BDC` *or* `BMC` and both count as marked. **Acceptance: zero unreachable operators.** This test found 24 orphaned operators — including the definition of a symbol used two paragraphs later — that no other check saw.
  3. **Artifact audit.** List what was marked as decoration. Only page furniture (page numbers, rules) belongs there. A table cell marked as an artifact vanishes entirely rather than degrading gracefully — e.g. the word `Quantum` disappearing so both rows of a Classical/Quantum comparison read as classical, one dropped word inverting the passage's meaning. **Acceptance: nothing meaningful is an artifact.**
  4. **Figure reading position.** Report where each `Figure` element falls in document reading order as a fraction of the whole. Figures must sit near the text they illustrate. **Acceptance: no figure clustered at the document end** (see the `[H]` requirement in 4b).
- **Acrobat rule-map sweep.** Acrobat's checker groups ~32 rules into Document / Page Content / Forms / Alternate Text / Tables / Lists / Headings. Walk the whole grid and record a status per rule, because the rules this pipeline fails are not the ones it worries about. A typical Acrobat report against this pipeline's output shows a pattern like **26 passed, 3 failed, 2 needs-manual-check, 1 skipped**, with the three failures being:
  - **Character encoding** — the `ToUnicode` problem. Fix at the font level (`unicode-math`), not by editing tags.
  - **Table headers** — a data table whose header row tagged as `TD`. Fix in the `tabular` markup.
  - **Lbl and LBody must be children of LI** — a list built by hand instead of with a list environment.
  Every one of these is a *source-markup* defect that a tag-editing pass would paper over and a rebuild would reintroduce. Fix them in the `.tex`, then rebuild — never by hand-patching the PDF, which the next compile discards.
- **Render a verdict on the three items no tool decides** (Principle 11). Each needs a written answer and its evidence, not a repeated "needs manual check":
  - **Logical reading order** — walk the tag tree in order and confirm it matches the intended reading of the physics: each figure adjacent to the derivation it serves, each equation between the lines that set it up and use it. State the walk you performed.
  - **Color contrast** — report measured ratios, not impressions: body text and link text against the page (**≥ 4.5:1**), figure ink and any rules or borders (**≥ 3:1**). Name the lowest *content* ratio in the document and where it occurs. Printed graph-paper ruling is paper, not content; exclude it from the verdict and say so. A "blue pen" layer that is <2 % of dark pixels is anti-aliased ruling — do not report it as pen.
  - **Table summary** — Acrobat *skips* this rule, which is not a pass. Either every data table has a `/Summary` **on the Table element** (not on a child TH), or the report says which ones do not and why. Confirm `/Scope` the way the kernel actually writes it (`/C /TH-col` + ClassMap), not by grepping for a direct `/Scope` key.
- **List and table structure counts.** Report the number of `L`, `LI`, `Lbl`, `LBody`, `Table`, `TR`, `TH` and `TD` elements, and confirm every `LI` has both a `Lbl` and an `LBody`, every `TR` sits under `Table`/`THead`/`TBody`/`TFoot`, and every data table has at least one `TH`. **Acceptance: no `LI` missing a child, no data table with zero `TH`.**
- **Math check.** Confirm `/Formula` elements exist and that the embedded MathML is well-formed **and non-empty**. Extract the MathML for the document's headline result and check it contains actual math tokens rather than a replacement character — boxed equations fail exactly here, and the failure is invisible to every other test. **Empty-MathML is an identity, not a count.** Map each Formula to its own `/AF` file; an empty Formula fails unless *that same* Formula carries `/ActualText` or `/Alt`. Comparing `len(spoken) >= len(empty)` is not a test. Do not classify emptiness by a hard-coded string such as "(all boxed)". Classify every U+FFFD by the Formula that owns it (boxed empty shell, `\xcancel`, `\cancel` stroke, oval-box decoration) and write that split in the log; "all in boxed shells" is not a safe assumption on this toolchain — verify it directly. **Run `tools/fix_pdf_mathml.py` before this check, not after** (it is a Stage 4b step, see the Command Reference) — a document that still has empty MathML at this point had the fix skipped, not a residual limitation to disclose. If it ever fires and the count of formulas fixed does not match expectations, that mismatch is itself reported here rather than silently trusted.
- **Alt-text audit.** Every figure has alt text that is specific, accurate to the drawing, and not a duplicate of the caption. Verify the strings embedded in the PDF against the sidecar. Generic strings ("figure", "diagram", "image of a graph") fail.
- **Metadata check.** Document language, real title, `DisplayDocTitle`, and the PDF/UA identifier are present.
- **Screen-reader spot-check.** Walk at least one full section as a screen reader would — heading navigation first, then linear read-through — and one equation-dense passage. State plainly whether the physics is followable without sight of the page.
- **HTML companion check.** MathML count, heading nesting with no skipped levels, a real `<h1>`, `<html lang>` set, every `img` alt, descriptive link text, `<th>` on data tables, real `<ul>`/`<ol>` markup, measured text contrast, and the count of equations rasterised rather than converted. Hold the HTML to **the same WCAG 2.1 AA bar as the PDF** — under Principle 12 it may be the artifact the recipient actually publishes, and it is the one the standard was written for. An accessible PDF shipped with a sloppy HTML sibling is half a deliverable. A `\noalign` row used to park `/Summary` in the PDF comes out of tex4ht as an empty `<tr>`; skip empty rows when promoting the header, or the real header stays `<td>`. Prefer `make4ht -u … "mathml"`; `-l` / `-f html5` have fatal'd on DVI in this toolchain.
- **Report honestly.** The verdict states what passed, what failed, and **what is known-partial**. Claiming conformance the tests did not confirm is a pipeline failure in its own right (Principle 10). Re-running the checker after a fix is **not** evidence of remediation if it was already passing — re-run the numeric tests above.
- **Loop condition:** failures return to Stage 4b (build/markup fixes) or Stage 1 (bad crop, missing alt text) and the document is rebuilt and re-checked. Expect the auditor to REVISE at least twice.

### Stage 5 — Hand-off package

The people who receive this work are not going to run the pipeline. Build them a
self-contained directory that stands on its own.

- **Contents:** the tagged PDF and its `.tex`; the style file and `alt_text.json`; the figures; the HTML companion; the conformance report and full auditor report; **the untouched source input**; the specification, run log and manifest; the tools; and the intermediate evidence (approved segments, segment manifest, review logs). **Every shipped file in the hand-off must be byte-identical to `Final_Product_Ready/`** (same MD5). A package that contains a different, older PDF is a failed Stage 5 even if the ready folder is correct.
- **A written report** that opens by stating plainly what was wrong before and what is *still* wrong now, ahead of anything it did well. List known-partial items explicitly — a reader who finds an unlisted defect will discount everything else in the document. It must also:
  - **Answer the receiving institution's checklist directly.** A recipient will ask whether this meets WCAG 2.1 AA, whether their institution's own faculty-facing skills list is covered, and whether it passes their institution's named checker — for this kit's institutional profile, a recipient at Ohio University asks whether the 7 Core Skills are covered and whether it passes PAC 2026. Give a row-by-row answer to each rather than a narrative that leaves them to infer it, and name which tools were actually run on which machine.
  - **Say which format the recipient should publish.** Per Principle 12, recommend the HTML companion where the delivery channel accepts it, with the tagged PDF as the archival and print copy — and explain the reasoning in one sentence so the choice is theirs to override.
  - **State the compliance context in one line, without alarm:** WCAG 2.1 AA, the legal basis that applies to the recipient (ADA Title II for a US public institution), and the recipient's own compliance date if one applies — for this kit's institutional profile, Ohio University's is April 26, 2027. The recipient needs the date to plan around, not a lecture about it.
- **A `verify.sh` the recipient can run themselves**, which re-runs the conformance check and the Step 4d numeric tests and prints the acceptance numbers. Include an install script for the toolchain, naming the minimum LaTeX version and why it matters.
- **Include the source input and the intermediate artifacts** so the recipient can audit the chain from their own material to the deliverable rather than taking the output on trust.

## Command Reference

Every mechanical step of the pipeline, in order, with the exact invocation to
run — demonstrated on the worked example shipped in
`Example_Deliverable_Directory/`. **Use these scripts rather than
reimplementing them** — each one encodes a defect that a review round has had
to catch once already, and a fresh implementation will very likely
reintroduce it. What no script does, and what the
rest of this file is about, is the judgement between the steps: choosing
seams, writing alt text, transcribing physics, and the review loops. Those are
agent work, not tool work.

`$SLUG` is the input's topic slug. Paths follow the Directory Conventions below.

**Stage 0 — archive any previous run, then register the input**

```bash
ts=$(date +%Y-%m-%d_%H%M%S)                       # archive before you run
mkdir -p Run_Archive/$ts
for d in segments staging assembled Final_Product_Ready; do
  [ -e "$d" ] && mv "$d" "Run_Archive/$ts/"
done
```

**Stage 1 — render, segment, check coverage, crop the figures**

```bash
# 1. Rasterise. The renderer is part of the measurement: every seam row and
#    crop box below is a pixel coordinate in THIS raster. pdftoppm is the
#    reference renderer; PyMuPDF disagrees with it pixel for pixel and even on
#    the page height. render.json records which engine and dpi were used.
python3 tools/render_pages.py input/<source>.pdf segments/$SLUG/pages --dpi 300

# 2. Cut segments on measured seams, protecting the diagram bands. The
#    --protect bands are "page:y0-y1" in page pixels and are the one argument
#    you must derive per document: find each drawing's row span first and
#    declare it un-cuttable, because a seam through a figure is the expensive
#    defect (that figure is also the deliverable's figure).
python3 tools/segment_seams.py 'segments/'$SLUG'/pages/page-*.png' \
    segments/$SLUG --target 780 --overlap 250 --min-h 300 --pad-top 40 \
    --protect "1:90-950,1:1495-2040,3:2015-2390,4:385-760"
# writes page01_seg01.png ... and segment_manifest.json (the authoritative
# inventory -- never infer the segment list from filenames)

# 3. Prove no ink was cut away. This gates Stage 2; it exits non-zero on loss
#    and names the uncovered row ranges.
python3 tools/check_coverage.py segments/$SLUG --pages segments/$SLUG/pages

# 4. Cut the figures. Boxes live in figure_crops.json keyed by final figure
#    filename; a figure needing more resolution carries its own render_dpi and
#    is cut from a page rendered at that dpi rather than upscaled.
python3 tools/render_pages.py input/<source>.pdf segments/$SLUG/pages600 --dpi 600 --pages 2
python3 tools/crop_figures.py staging/$SLUG/figure_crops.json \
    segments/$SLUG/pages staging/$SLUG/figures --extra-pages 600=segments/$SLUG/pages600

# 5. Measure crop contrast (WCAG 1.4.11, >= 3:1) and record before/after in the
#    manifest for anything you had to raise.
python3 tools/check_contrast.py --images staging/$SLUG/figures \
    --json staging/$SLUG/contrast_figures.json
```

`alt_text.json` is written **by hand at crop time**, keyed by final figure
filename, while the drawing is in front of you. No script drafts it; the build
fails if it is missing.

**Stage 3 — assemble the approved segments**

```bash
python3 tools/assemble_pdf.py segments/$SLUG assembled/${SLUG}_approved.pdf \
    --title "<topic>"
```

**Stage 4b — tag the transcription and compile**

`staging/$SLUG/notes_src.tex` is the agent's transcription: plain LaTeX, no
metadata block. `make_accessible.py` turns it into the tagged document —
`\DocumentMetadata`, OpenType math, `[H]` on every float, `alt=` pulled from
the sidecar — and **fails the build if any figure lacks alt text**.

```bash
python3 tools/make_accessible.py \
    staging/$SLUG/notes_src.tex Final_Product_Ready/$SLUG.tex \
    staging/$SLUG/alt_text.json \
    --title "<document title>" --author "<course -- instructor>" --modern

cd Final_Product_Ready
for i in 1 2 3; do lualatex -interaction=nonstopmode $SLUG.tex; done
```

Three passes, always: luamml writes MathML fragments on one pass and embeds
them on a later one, so a two-pass build ships `/Formula` elements with no
mathematics attached. **LuaLaTeX exits non-zero on recovered errors and still
writes a complete PDF** — under `set -e` that reads as a build failure when it
is not, and read the other way it hides a misfiring macro. Count them
(`grep -c '^! ' build.log`) and treat a non-zero count as something to explain.

**Stage 4b — HTML + MathML companion** (required sibling, not a by-product)

```bash
# strip \DocumentMetadata, unicode-math and \setmathfont into a tex4ht-safe
# copy first -- they fatal under make4ht -- then:
make4ht -u notes "mathml"
python3 tools/fix_html_alt.py notes.html staging/$SLUG/alt_text.json
python3 tools/fix_html_structure.py notes.html
```

`make4ht -l` and `-f html5` have fatal'd on DVI in this toolchain; `-u … "mathml"`
is the route that works. `fix_html_alt.py` also reports how many equations were
rasterised rather than converted — that count is the honest measure of what the
HTML route failed to make accessible.

**Stage 4b — splice real MathML into boxed/xcancel Formulas** (closes the
empty-MathML gap; run after the HTML companion above exists)

```bash
python3 tools/fix_pdf_mathml.py Final_Product_Ready/$SLUG.pdf \
    Final_Product_Ready/html/notes.html --in-place
```

Finds every Formula whose `/AF` MathML is an empty U+FFFD shell (a box or an
`\xcancel` defeated LuaTeX's tagger) and replaces the placeholder with the real
content lifted from the HTML companion, matched by equation number (or, for an
unnumbered `\xcancel`, by its unique double-strike notation) — see **On known
limitations** below for why this is an identity match rather than a guess.
Fails loudly if the count of formulas it fixed does not equal the count of
boxed/ovaled equation numbers it was told to expect plus one, so a future
change to the boxing macros or the HTML build cannot silently stop working.

**Stage 4b — patch latex-lab tagging defaults** (closes PAC 2026
false-negatives and semantically-wrong RoleMap defaults; run any time after
the compile, order-independent with the MathML splice above)

```bash
python3 tools/fix_pdf_tagging_defaults.py Final_Product_Ready/$SLUG.pdf --in-place
```

Fixes four defects, found by walking the PDF's own `/RoleMap`, `/ClassMap`
and `StructElem` dicts with pikepdf and cross-checking against a detailed
PAC 2026 report (not just its summary page) — each confirmed at the
attribute level, not assumed from PAC's characterization alone:

1. Every `TH` cell carries `/Scope` only through `/C /TH-col` +
   `/ClassMap` — conformant PDF and this pipeline's deliberate choice (a
   checker that only looks for a *direct* `/Scope` key false-negatives
   otherwise, see Step 4b above), but PAC 2026 appears to be exactly that
   checker. The script adds a literal `/A` duplicating the `ClassMap`-
   resolved dict directly on each `TH`, redundant with `/C` but readable
   either way.
2. `RoleMap /text-unit → /Part` and `/float → /Note` are `tagpdf-ns-latex-
   lab.def`'s own built-in defaults — every ordinary paragraph is wrapped
   `text-unit` (so registers as a `/Part`, the role for top-level book
   divisions, once per paragraph) and every figure/table float environment
   is wrapped `float` (registers as `/Note`). Neither is a choice this
   document's `.sty` or transcription made. The script remaps them to `/P`
   (matching this document's existing `text → /P` mapping) and `/Div`.
3. Every `Table`'s `/Summary` was a bare top-level `StructElem` key —
   not a valid PDF structure-element key under ISO 32000 at all; the spec's
   table attributes live inside `/A` with `/O /Table`, exactly like `/Scope`
   does for `TH` in (1). `check_structure.py`'s own test only checked
   presence anywhere on the element, so this shipped undetected for months
   and plausibly explains PAC flagging 3/3 Tables "possibly inappropriate
   use" with no other attribute-level cause found. The script promotes the
   existing text into a proper `/A << /O /Table /Summary (...) >>`,
   additive alongside the legacy key.
4. `L` (enumerate) elements carry `/C /enumerate` → `/ClassMap` →
   `<</O /List /ListNumbering /Ordered>>` — the same ClassMap-only-attribute
   pattern as (1), applied to lists instead of table headers. The script
   adds the same kind of literal `/A`.

(A fifth candidate — Formula elements' `/C /display`/`/inline` also resolve
only through `/ClassMap` — was investigated and **not** fixed: both classes
use the identical mechanism, but PAC flags 52/52 display Formulas and 0/146
inline, so an unresolved-ClassMap theory is contradicted by the very data
that would need to support it. Documented as a tested dead end so a future
run does not re-investigate it.)

Fails loudly (refuses to save) if the `RoleMap`/`ClassMap`/`StructElem`
shape any of these four expect is not present, rather than silently doing
nothing. Verify afterward exactly like the MathML fix: re-run veraPDF (both
profiles should show the identical clause set as before — these patches
change semantics, not conformance pass/fail) and `check_structure.py` (the
`Part`/`Note` element-type counts should be zero; `P`/`Div` should have
grown by the same amount; `tables_summary_not_in_A` should be empty —
verify this specific field actually fails against a pre-fix build before
trusting it to pass a post-fix one).

On the worked example in `Example_Deliverable_Directory/`, applying this
script moves `Part` 57→0, `Note` 8→0, `P` 115→173, `Div` 12→20, `TH`
unchanged at 7 with `/A` now present on all of them, all 3 `Table`s'
`/Summary` promoted into `/A`, and both `L` elements given a direct `/A`;
veraPDF UA-1 (this document's declared standard, see above) stays PASS
throughout.

**Stage 4d — measure the built PDF**

```bash
verapdf -f ua1 --format text Final_Product_Ready/$SLUG.pdf   # and again with -f ua2
python3 tools/check_structure.py Final_Product_Ready/$SLUG.pdf \
    --alt staging/$SLUG/alt_text.json --sections <N> \
    --json Final_Product_Ready/accessibility/structure_tests.json
python3 tools/check_contrast.py --pdf Final_Product_Ready/$SLUG.pdf \
    --json Final_Product_Ready/accessibility/contrast_pdf.json
```

`--sections <N>` is the heading count taken from the `.tex` outline
(`grep -cE '^\\(sub)*section\{' notes.tex`). The inventory test compares the
PDF against that number, so reading the number off the PDF defeats the test.
`\maketitle` contributes a heading of its own, so N is the sectioning-command
count plus one: in the worked example (`Example_Deliverable_Directory/`),
4 + 9 + 2 sectioning commands plus the title give `--sections 16`, and the
PDF carries exactly 16 H-elements.

**Stage 5 — verify the package the recipient will receive**

```bash
./verify.sh /path/to/verapdf      # re-runs the conformance check and all of 4d
```

**Checking a Stage 1 run is deterministic.** Re-render, re-cut and re-crop
from the source PDF and compare against what is already on disk: identical
output means the stage is reproducible, and `crop_figures.py --check` and
`check_coverage.py` both exit non-zero when it is not.

```bash
python3 tools/crop_figures.py staging/$SLUG/figure_crops.json \
    segments/$SLUG/pages staging/$SLUG/figures --check
```

---

## Directory Conventions

```
project_root/
├── input/                 # Stage 0: source handwritten/board PDFs (one per topic)
├── segments/
│   ├── <slug-a>/          # Stage 1–2: segmented PNGs, segment_manifest.json, alt_text.json
│   └── <slug-b>/          #            ... for input B
├── assembled/             # Stage 3: one assembled PDF per input (<slug>.pdf)
├── Final_Product_Ready/   # Stage 4: one .tex + one tagged PDF per input
│   ├── html/              #   Step 4b: HTML + MathML companion per input
│   └── accessibility/     #   Step 4d: conformance report + auditor verdict per input
├── For<Recipient>/        # Stage 5: self-contained hand-off package
├── refs/                  # governing-standard sources (OU accessibility PDFs, sources.md)
├── tools/                 # reusable scripts (see Reuse Notes)
└── Run_Archive/           # Pre-flight: archived directories from previous jobs (timestamped)
```

Everything downstream of Stage 0 is **partitioned by input slug** — segments, assembled PDFs, and final documents each carry the slug of the input they came from, so the 1:1 input→output mapping is visible in the file tree.

(Only `Final_Product_Ready/` is a required name from the original plan; the rest are suggested and may be renamed.)

---

## Success Criteria

1. Any directories left over from previous jobs were archived before the run started.
2. Every source page is represented by legible, well-segmented PNGs.
3. All 3 reviewer agents have approved the segments (review loop closed).
4. An assembled PDF of approved segments exists **for each input**.
5. `Final_Product_Ready/` contains a `.tex` source and a cleanly compiled, **tagged** LaTeX PDF **for each input**.
6. **The input→output mapping is 1:1:** the number of final PDFs equals the number of input PDFs, no two inputs were merged into one document, and no single input was split across documents.
7. The `.tex` document uses the notation conventions of an explicitly named reference textbook that best matches the notes' subject matter (Stage 4a), the textbook was used for context and notation only, and that choice was reviewed and justified.
8. The final PDF is predominantly the source content, with additions only where a step would otherwise be unfollowable and each addition kept very concise.
9. **No output document contains any reference to notes, boards, lectures, pages, scans, or handwriting** — in body text, captions, footnotes, or headings.
10. Each final PDF opens directly with the content — no introduction about the agents or pipeline.
11. **Every figure in every final PDF is a high-fidelity image crop of the corresponding source drawing** — no redrawn or substitute diagrams — and each caption conveys the original drawing's intention (what it illustrates and why) in the document's own voice.
12. All 5 final-review agents have approved every compiled LaTeX PDF as **publication-ready by a major physics publisher's standard** in typesetting quality (Stage 4 loop closed).
13. When multiple input PDFs were supplied, they were processed in parallel by subagent chains without loss of quality.
14. **Every final PDF is tagged**, built with LuaLaTeX (TeX Live 2024+) under `\DocumentMetadata`, with a declared language and title. An untagged PDF fails the run outright.
15. **Every figure in every final PDF carries non-empty, meaningful alt text** that describes the drawing's content and is distinct from its caption.
16. **A conformance report exists for every output document** in `Final_Product_Ready/accessibility/`, produced by an actual checker rather than asserted by an agent, and the **Accessibility Auditor has approved** each document independently of the physics reviewers.
17. **An HTML + MathML companion exists for every output document**, and every known accessibility gap is stated plainly in the run log rather than left implied.
18. **The four Step 4d numeric tests were run and recorded**, with these results: headings 1:1 with the source outline; **zero** text operators unreachable from the tag tree; nothing meaningful marked as an artifact; and no figure clustered at the end of reading order. A checker pass alone does not satisfy this criterion.
19. **`/Formula` elements exist and their MathML is non-empty** — verified by extracting the headline equation, not inferred from the element count. Any equation whose MathML is empty is named in the run log.
20. **Source errata are handled by one consistent policy** across the whole document: transcribed as written and flagged, never silently corrected and never silently propagated.
21. **A hand-off package exists** (Stage 5) containing the deliverable, the evidence, the source input, the reproduction instructions and a runnable verification script, with a report that states the remaining defects up front.
22. **Every item of the receiving institution's floor checklist is individually confirmed and recorded** for every output document — for this kit's institutional profile, Ohio University's MDAS five: permission flag set, title present, full text present, language specified, alt text on every figure.
23. **Every row of the receiving institution's faculty-facing skills checklist is answered** for every output document — satisfied, or explicitly marked not-applicable with a reason. A blank row is a failed criterion, not an omission. (Worked example: Ohio University's 7 Core Skills table.)
24. **Lists and tables are structurally sound:** every `LI` has both a `Lbl` and an `LBody`, every data table has at least one `TH` and a summary, and no table is used for visual layout.
25. **Link text is descriptive throughout** and every link annotation carries `/Contents`; no "click here" and no bare URLs in running text.
26. **Bookmarks/outline exist and mirror the heading structure**, and tab order follows structure order.
27. **Contrast was measured, not estimated:** the lowest measured ratio in each document is recorded, with text ≥ 4.5:1 and figure ink, rules and borders ≥ 3:1; where a source crop had to be adjusted to reach 3:1, the before/after ratios are in `segment_manifest.json` and the drawing itself was preserved.
28. **The three unautomatable checks carry explicit written verdicts** — logical reading order, color contrast, and table summary. A shipped report containing an unresolved "needs manual check" or "skipped" fails this criterion.
29. **The HTML companion meets the same WCAG 2.1 AA bar as the PDF**, and the hand-off report states which of the two the recipient should publish and why.
30. **The tooling actually used is named honestly** — veraPDF always; the receiving institution's named checker (Ohio University: PAC 2026) and/or Acrobat where they were available, with the absence stated plainly where they were not.
31. **Empty MathML is identity-matched.** Every empty `/AF` Formula is named, and each of those Formulas (not a matching count of other Formulas) carries `/ActualText` or `/Alt`. The log's U+FFFD split matches an independent Formula→`/AF` count.
32. **Every data-table `/Summary` sits on the Table element, inside `/A` with `/O /Table`** — not on a TH, and not as a bare top-level `StructElem` key (spec-invalid, satisfies nothing per ISO 32000 even though it may look present to a naive check); every TH carries column scope the way the kernel writes it (`/C /TH-col` + ClassMap), promoted into a direct `/A` too. Caption–`\toprule` ink gap is ≥ 6 pt on every data table.
33. **The Stage 2 review log records an explicit APPROVE or REVISE for every reviewer in every round.** "Verdicts: see below" with nothing below does not satisfy criterion 3.
34. **The hand-off PDF is byte-identical to the `Final_Product_Ready/` PDF** (same MD5). Logs, the manifest and the auditor report describe that same hash.
35. **One Stage 4c referee audited claims against measurements** and found no live false claim about the frozen build. Recantations of earlier drafts are allowed; current-state lies are not.

---

## Reuse Notes

- This outline is a **rough-draft template**: anyone should be able to reuse it by pointing Stage 0 at their own PDFs and re-running the pipeline.
- The segmentation skill (Stage 1), the reviewer agent prompts (Stage 2), and the assembly/compilation steps (Stages 3–4) should each be built as separable, reusable components so the process works universally across courses, note styles, and subjects.
- The number and specialty of reviewer agents (default: 3 × physics PhD) is configurable — adjust to match the subject matter of the notes.
- The 1:1 input→output rule is what makes the pipeline scale: drop *n* topic PDFs into `input/`, get *n* self-contained documents back. Batching topics into one file is never the right call, even when the topics are related.
- The reference-textbook convention (Stage 4a) generalizes too: for non-physics notes, match against the standard textbook of that field and hold the final PDF to the same publication-ready bar from that field's major publishers.
- **The accessibility layer is subject-independent and should be reused verbatim.** Tagged output, alt text, verified conformance, and the HTML companion apply to any course in any field. Only the alt-text *content* is domain-specific — the Stage 1 drafting step and the Stage 4d verification step carry over unchanged. Where a field leans less on equations, the tagged PDF alone may suffice and the HTML companion becomes optional rather than required.

**Reusable scripts** (in `tools/`, all subject-independent):

| Script | Does |
|---|---|
| `render_pages.py` | Stage 1 step 0: PDF → page rasters at a stated dpi. Prefers `pdftoppm` (the reference renderer, reproduces its rasters bit for bit) and records the engine in `render.json`, because seam rows and crop boxes are coordinates in one particular raster and two rasterisers do not agree. |
| `crop_figures.py` | cuts the deliverable's figures from the page rasters per `figure_crops.json`, honouring a per-figure `render_dpi`; `--check` re-cuts and compares pixel by pixel instead of writing |
| `segment_notes.py` | whitespace-valley segmentation with overlap and ruling suppression |
| `segment_seams.py` | ink-mask + seam placement; the mask must capture saturated colour (see Stage 1) |
| `assemble_pdf.py` | Stage 3 assembly of approved segments |
| `make_accessible.py` | turns a plain `.tex` into a tagged one: metadata, native `alt=` from the JSON sidecar, `[H]` figure pinning, OpenType math. **Fails the build if any figure lacks alt text.** |
| `fix_html_alt.py` | repairs `make4ht`'s `alt="PIC"` and counts rasterised equations |
| `fix_html_structure.py` | heading-level remap, real `<th>` on the first non-empty data-table row (skip `\noalign` empties), captions, `role=presentation` on layout tables, `dl.enumerate` → `<ol>` |
| `check_contrast.py` | ink-vs-background ratio on each figure crop and text/link contrast in the built PDF; reports the document's lowest *content* ratio. Ignore a "pen" layer that is <2 % of dark pixels (anti-aliased ruling registering as blue pen). Classify on green. Use the layer's representative (median) colour, not its darkest tail. |
| `check_structure.py` | Step 4d element inventory, MCID reachability (artifact wins over nesting), artifact audit (decodes hex CID strings), figure reading position, `L`/`LI`/`Lbl`/`LBody` and `Table`/`TH` counts, table `/Summary` **on the Table and inside `/A`** (`tables_summary_not_in_A` — a bare-key-only `/Summary` is spec-invalid and can otherwise ship undetected; verify this test against a known-bad build before trusting it clean), empty-MathML **identity-matched to that Formula**, alt-text vs sidecar, metadata. |
| `check_coverage.py` | ink **row coverage**: every ink row inside the page's content band must fall inside at least one segment span from the manifest. Exits non-zero and names the uncovered row ranges. (It formerly compared ink *mass*, which overlap inflates by 20–40 %, so it could not fail; that version's pass meant nothing.) |
| `fix_pdf_mathml.py` | closes the boxed/`\xcancel` empty-MathML gap: matches each empty `/AF` Formula to the real MathML tex4ht generated for the same equation in the HTML companion (by equation number, or by strike notation for an unnumbered `\xcancel`) and splices it in. Fails loudly on a count mismatch rather than silently fixing fewer than expected. |
| `fix_pdf_tagging_defaults.py` | patches four `latex-lab`/`tagpdf` kernel defaults, found via a real PAC 2026 detailed report across two rounds: adds a literal `/A` to every `TH` cell duplicating what `/ClassMap /TH-col` already resolves to (fixes a "no associated data cells" false negative); remaps `RoleMap /text-unit → /P` and `/float → /Div` (both default to a semantically wrong standard role — `/Part`, `/Note` — for every paragraph/float, not this document's choice); promotes every `Table`'s `/Summary` from a spec-invalid bare `StructElem` key into a proper `/A << /O /Table /Summary >>`; adds a literal `/A` to every `L` (enumerate) element duplicating what `/ClassMap /enumerate` resolves to. Additive/redirective only; refuses to save if the `RoleMap`/`ClassMap`/`StructElem` shape any of the four expects is missing. |

**These checks' pass rules are part of the spec, not a courtesy.** A checker that compares counts instead of identities, that hard-codes a classification, or that cannot fail, is a defect in the pipeline, not a pass of the document. Verify that each one *can* fail before you trust that it passed: break the input on purpose — delete a segment from the manifest, empty an alt string — and confirm the checker says so.

- **On known limitations, and the fix for the boxed/xcancel gap.** A current LaTeX kernel tags mathematics well. The remaining gap is specific rather than general — **boxed** display math, `\xcancel` over mathematics, and oval-box decoration export MathML with no content or inject U+FFFD, and no box variant avoids it at the LuaTeX level. `\cancel` strokes inject U+FFFD into otherwise well-formed MathML. **This is now closed, not just disclosed, by `tools/fix_pdf_mathml.py`.** The mechanism: `\boxed`/`\ovalbox` hide their contents from LuaTeX's own math tagger (an opaque picture to it), but the required HTML + MathML companion is built by a completely different route (`make4ht`/tex4ht) that never runs that tagger — it renders `\boxed` as MathML `<menclose notation='box'>` and `\xcancel` as `<menclose notation='updiagonalstrike downdiagonalstrike'>`, both with the real math content intact, because tex4ht's math-to-MathML conversion does not go blind inside a box the way the PDF math tagger does. Since the HTML and PDF are compiled from the same `.tex` source, the fix is an exact identity match, not a position guess: numbered boxed/ovaled results are matched to the HTML by equation number (`<td class='eq-no'>(N)</td>`, which tex4ht writes next to every numbered display); an unnumbered `\xcancel` is matched by its unique `updiagonalstrike downdiagonalstrike` notation. Run it as the last step of Stage 4b, **after** the three-pass LuaLaTeX compile and **after** the HTML companion build (it reads both): `python3 tools/fix_pdf_mathml.py Final_Product_Ready/$SLUG.pdf Final_Product_Ready/html/notes.html --in-place`. Verified on the worked example in `Example_Deliverable_Directory/`: `check_structure.py`'s `mathml_empty` count goes from 8 to **0** with no other Formula touched, veraPDF UA-2 stays **PASS**, and UA-1's pre-existing failed-checks count for a document declaring UA-2 at all (an artifact of that declaration, not of this fix) is identical before and after. Ship the HTML companion regardless — it remains the fallback for any future macro that defeats the tagger the same way — and never claim conformance the numeric tests have not confirmed.
- **The most transferable lesson behind this whole toolchain:** every serious defect is found by *measuring the output*, not by reading the source or trusting a tool — including this pipeline's own tools. Silent degradation is the normal failure mode across this whole toolchain — ignored `testphase` modules, a dropped `alt` key, a legacy glyph macro producing nothing, floats relocating their own structure, boxes swallowing MathML, an ink mask that cannot see red, a `/Summary` that landed on TH, a checker that compared counts. None of these raised an error, and several of them passed the conformance checker *and* the in-house scripts. Build the numeric checks first, let them gate the pipeline, and have one referee whose only job is to catch the scripts lying.
- **This document already separates the universal layer from the institutional one — use that structure when porting it.** WCAG 2.1 AA, PDF/UA, the Step 4d numeric tests and the Acrobat rule map are the standard and travel unchanged to any institution (Governing Standard → Universal core). What is local to Ohio University is the *packaging* — the 7 Core Skills framing, the MDAS five, PAC 2026 as the named tool, the April 26, 2027 date, and the reduce-PDFs format preference (Governing Standard → Worked institutional profile, and Appendix: Worked Institutional Profile). At another institution, swap that packaging for theirs and leave the technical layer (this whole document, minus that one section) alone — and read your own institution's guidance directly rather than assuming it matches Ohio's, because the framing is what your recipient will actually grade you against.

---

## Appendix: Worked Institutional Profile — Ohio University

This appendix backs the **Worked institutional profile** subsection of Governing Standard. It is kept as a complete, concrete example — not because Ohio University's requirements bind any other run of this pipeline, but because a fully worked profile is what makes building your own institution's version fast: archive your institution's equivalent policy documents under `refs/<your-institution>-accessibility-sources/`, build a table like the one below, and update the Worked institutional profile subsection with your own institution's legal basis, faculty checklist, named checker, format guidance, and floor list. Everything else in this file — Stages 0 through 5, every tool, every principle — needs no change to run against a different institution.

The Governing Standard section's institutional profile is derived from these, archived under `refs/OU-accessibility-sources/` (originals: `TA_Tasks/OU-accessibility-sources.zip` in the Ohio University OneDrive; snapshots taken 2026-08-08).

| File | What it establishes |
|---|---|
| `01_OU-news-DOJ-extension-260505.pdf` | Ohio University's compliance date moved to **April 26, 2027**; requirements unchanged; cross-campus working group coordinating |
| `02_OU-news-faculty-deadline-260200.pdf` | Faculty scope (Canvas content, documents and PDFs, web materials, media, images/tables) and the **7 Core Skills** |
| `03_OU-OIT-digital-accessibility-guidelines.pdf` | OHIO adopts **WCAG 2.1 AA** (50 A+AA criteria) as its primary technical standard; WAI-ARIA 1.2; **WCAG2ICT** for non-web content |
| `04_OU-OIT-accessible-documents.pdf` | The PDF-specific guidance: reduce PDFs, prefer other formats, **PAC 2026** via Company Portal (Windows), OCR before remediation, **no in-house remediation service** |
| `05_OU-OIT-faculty-course-checklist.pdf` | The 13-item faculty checklist — alt text, readable text and colors, descriptive links, run the checker, accessible PDFs or alternatives, simple tables, clear language, no blinking content |
| `06_FederalRegister-Title-II-deadline-extension.pdf` | The DOJ Interim Final Rule (April 20, 2026) itself — the primary legal source for the dates and the WCAG 2.1 AA standard |
| `TA_acc_image.png` | A real Acrobat accessibility report from this toolchain: 26 passed / 3 failed / 2 needs-manual-check / 1 skipped — the source of the rule-map sweep in Step 4d |

Two further OHIO sources inform this document and are worth reading alongside the above:

- **`Creating an Accessible ETD (LaTeX)`** (Thesis & Dissertation Services, Graduate College) — the origin of the **MDAS** five and of the practice of attaching the accessibility report to the submitted PDF. Note that its Acrobat procedure deliberately enables only four Document-category checks; that narrow subset is right for ETD submission and **wrong for this pipeline**, which runs the full rule set.
- **`sources.md`** inside the archive — records provenance and capture method for each snapshot.

None of the OHIO sources address mathematics, LaTeX, or STEM notation. Everything in this document about tagged math, MathML, `unicode-math` and boxed equations is this pipeline's own work and has no institutional guidance behind it — which is precisely why Step 4d measures it rather than citing it.
