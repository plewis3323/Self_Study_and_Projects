# Multi-Agent Pipeline: Handwritten Notes → LaTeX PDF

## Project Goal

Build a reusable multi-agent framework that converts handwritten notes (paper, whiteboard, or chalkboard photos/scans in PDF form) into legible, well-segmented, LaTeX-compiled PDF outputs.

This document is the master plan for the first pass. It is written to be **agent-readable**: an orchestrating agent should be able to read this file and execute the pipeline stages in order. It is also meant to be **edited and reused** — swap in your own input files, agent counts, or output conventions as needed.

---

## Agents

| Agent | Role |
|-------|------|
| **Prime Agent** (orchestrator) | Runs the pipeline end to end: ingests input PDFs, performs segmentation, submits work for review, applies feedback, assembles final outputs. |
| **Reviewer Agents ×3** (physics-PhD-level experts) | Independently inspect the segmented PNG outputs for legibility, correct segmentation, and faithful capture of the physics/math content. Each returns explicit feedback and an APPROVE / REVISE verdict. |
| **Final Review Agents ×5** (physics-PhD-level experts) | Independently inspect the compiled LaTeX PDF from Stage 5 for correctness, legibility, and fidelity to the source notes. They also act as journal/publisher referees: they heavily scrutinize whether the document follows the typesetting conventions of the reference textbook chosen in Stage 5 and whether it is **publication-ready by a major physics publisher's standard** — i.e., it reads like a section of a serious physics textbook or paper, not like transcribed notes. Each returns abundant, scrutinized feedback until all five approve. |

---

## Pipeline Stages

### Stage 0 — Ingest
Feed the handwritten / board-written PDF files into the framework.

- **Input:** one or more source PDFs (handwritten pages, whiteboard/chalkboard photos).
- **Action:** register the files, verify they are readable, and stage them for segmentation.

### Stage 1 — Segment to PNG
Create (or invoke) a **segmentation skill/extension** that splits each page into legible, readable PNG files.

- Segment by logical unit (equation block, diagram, paragraph of notes) so each PNG is independently readable.
- **Overlap is allowed and encouraged** where it improves readability — adjacent segments may share content rather than cutting a figure or equation in half.
- **Output:** a set of PNG files per source page, with a naming scheme that preserves page order and segment order (e.g. `page03_seg02.png`).

### Stage 2 — Expert Review Loop
The Prime Agent's PNG output is scrutinized by the **3 physics-PhD-level reviewer agents**.

- Each reviewer examines every PNG for legibility, segmentation quality, and content fidelity, and returns concrete feedback.
- Reviewers must be PhD-level physics experts and act as heavily strict, serious critics — scrutinizing the segmentation, the underlying physics, and the logic of the material.
- Reviewers also check that segment overlap is used correctly: enough overlap to avoid losing information at segment boundaries, without being excessive.
- **Loop condition:** Stages 1 ↔ 2 repeat — the Prime Agent re-segments per the feedback — until **all reviewers approve**. Only then does the pipeline advance.
- Keep a short log of each review round (round number, feedback given, changes made) so the loop is auditable.

### Stage 3 — Assemble Reviewed PDF
Paste the approved PNGs, in order, into a single compiled PDF.

- **Output:** one PDF containing all approved segments in reading order.

### Stage 4 — Mathpix-Ready Staging (Alternate Path A)
Copy the final pictures and the assembled PDF into a directory named **`mathpix_ready/`** (create it if it does not exist).

- **Verify** the contents actually meet Mathpix input requirements (supported formats, resolution, file sizes) — don't just copy blindly.
- **Alternate path:** these files can be sent to Mathpix to produce a `.tex` document, which a separate AI agent then cleans up/fixes and compiles to PDF. This branch is optional and runs outside this pipeline.

### Stage 5 — Direct LaTeX Compilation (Primary Path B)
Instead of (or in addition to) the Mathpix route: take the final PDF / pictures and produce a **LaTeX-compiled PDF** directly.

**Step 5a — Choose the reference textbook convention (before writing any LaTeX):**

- The Prime Agent first identifies the standard physics textbook(s) whose subject matter **best matches the content of the class notes** (e.g., Griffiths for E&M or QM, Taylor for classical mechanics, Jackson for graduate E&M, Sakurai for graduate QM, Kittel/Ashcroft & Mermin for solid state).
- The chosen textbook's **conventions become the style contract** for the entire document, and this choice must itself be **heavily scrutinized**: the Prime Agent must state which textbook(s) it chose, why they best match the notes, and the reviewer agents must challenge that choice before transcription begins.
- "Convention" means, concretely: notation (symbols, vector/tensor notation, unit system such as SI vs. Gaussian), equation formatting and numbering, theorem/definition/example environments, section and subsection structure, figure and table captioning, and the overall pedagogical voice of the matched textbook.

**Step 5b — Transcribe and compile in that convention:**

- Transcribe the approved content into a `.tex` document **written throughout in the chosen textbook's convention** — not a raw transcription of the handwriting, but the same material as it would appear typeset in that textbook.
- Compile it and confirm it builds cleanly (no errors, no unresolved references, no overfull-box sloppiness in the final PDF).

**Step 5c — Publication-readiness review:**

- Once compiled, **5 physics-PhD-level agents** heavily scrutinize the result and give abundant, rigorous feedback.
- The evaluation bar is explicit and strict: the final product must be judged **publication-ready by the standard of a major physics publisher** (e.g., Springer, Cambridge University Press, Pearson, APS journals). The compiled PDF should look like **notes/sections from a serious physics textbook or a professional physics paper** — in typography, notation consistency, logical flow, and physical correctness.
- Each reviewer must explicitly verify and report on **both**: (1) fidelity to the source notes' content, and (2) adherence to the reference textbook's conventions and publisher-grade typesetting quality. Anything that reads as "transcribed homework" rather than "typeset textbook" is grounds for a REVISE verdict.
- **Loop condition:** if any expert requests changes, the pipeline is re-run from the appropriate earlier stage until **all 5 experts agree** the compiled PDF is correct **and publication-ready**.
- Between rounds, the Prime Agent revises by re-reading the original notes and consulting the web or its training data on the underlying physics — to better understand the content and resolve the experts' feedback before the next review pass.
- Place the `.tex` source and compiled PDF into **`Final_Product_Ready/`** (create it if it does not exist).

---

## Directory Conventions

```
project_root/
├── input/                 # Stage 0: source handwritten/board PDFs
├── segments/              # Stage 1–2: segmented PNGs (per review round)
├── assembled/             # Stage 3: reviewed, assembled PDF
├── mathpix_ready/         # Stage 4: verified Mathpix-ready files (alt path)
└── Final_Product_Ready/   # Stage 5: final .tex + compiled LaTeX PDF
```

(Only `mathpix_ready/` and `Final_Product_Ready/` are required names from the original plan; the rest are suggested and may be renamed.)

---

## Success Criteria

1. Every source page is represented by legible, well-segmented PNGs.
2. All 3 reviewer agents have approved the segments (review loop closed).
3. An assembled PDF of approved segments exists.
4. `mathpix_ready/` contains verified, Mathpix-compatible copies of the final assets.
5. `Final_Product_Ready/` contains a `.tex` source and a cleanly compiled LaTeX PDF.
6. The `.tex` document follows the conventions of an explicitly named reference textbook that best matches the notes' subject matter (Stage 5a), and that choice was reviewed and justified.
7. All 5 final-review agents have approved the compiled LaTeX PDF as **publication-ready by a major physics publisher's standard** — it reads like a serious physics textbook or paper (Stage 5 loop closed).

---

## Reuse Notes

- This outline is a **rough-draft template**: anyone should be able to reuse it by pointing Stage 0 at their own PDFs and re-running the pipeline.
- The segmentation skill (Stage 1), the reviewer agent prompts (Stage 2), and the assembly/compilation steps (Stages 3–5) should each be built as separable, reusable components so the process works universally across courses, note styles, and subjects.
- The number and specialty of reviewer agents (default: 3 × physics PhD) is configurable — adjust to match the subject matter of the notes.
- The reference-textbook convention (Stage 5a) generalizes too: for non-physics notes, match against the standard textbook of that field and hold the final PDF to the same publication-ready bar from that field's major publishers.
