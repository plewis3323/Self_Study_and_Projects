# Full Pipeline Prompt: Raw Notes → OrganizedNotes → LaTeX/PDF

Use this document as a **single end-to-end workflow prompt** for converting graduate-level physics handwritten lecture notes into a compilable LaTeX document and PDF.

For step-specific system prompts, see the linked files at the bottom. This file describes the **full process** and how to run it in Cursor or manually.

---

## Goal

Convert disorganized professor lecture notes (paper scans, whiteboard photos, PDF exports) into:

1. An **OrganizedNotes** package (Step 1) — AI-readable structure with handwriting preserved
2. A **single `.tex` file** and **PDF** (Step 3b) — readable, reproducible lecture notes

**Alternative:** Step 3a (Mathpix OCR per block) instead of Step 3b. This prompt focuses on the path we validated: **Step 1 → Step 3b**.

---

## Pipeline overview

| Step | Name | Input | Output |
|------|------|-------|--------|
| **0** | Raw notes | Paper, whiteboard, PDF | Unorganized images/PDF |
| **1** | OrganizedNotes | Raw source files | `OrganizedNotes/<lecture_id>/` package |
| **3a** | Mathpix OCR | Block `image.png` files | Raw `.tex` per block → merged PDF |
| **3b** | Direct LaTeX | Manifest + meta + block images | Single `.tex` → PDF |

There is **no separate Step 2**. After Step 1, choose **3a** or **3b**.

---

## End-to-end workflow (copy this block to an agent)

```
Run the full physics-notes pipeline on my lecture source material:

STEP 1 — OrganizedNotes (physics-notes-organizer)
- Ingest all source pages unchanged into OrganizedNotes/<lecture_id>/source/
- Segment into logical blocks (definitions, derivations, equations, diagrams, remarks)
- Crop each block to blocks/block_NNN/image.png (handwriting preserved)
- Write manifest.yaml and blocks/block_NNN/meta.yaml per schema
- Validate: every source page referenced, reading_order complete, no dropped blocks

STEP 3b — Direct LaTeX
- Read manifest.yaml and all block meta.yaml files in reading_order
- Treat block images as authoritative for notation when present
- Produce OrganizedNotes/<lecture_id>/output/<lecture_id>.tex
- Follow manifest sections; add % block_NNN traceability comments
- Add % REVIEW: flags for confidence low/medium blocks
- Compile with pdflatex (two passes) → PDF
- Write output/TRIAL_REPORT.md with validation checklist

Do not invent physics beyond what the blocks support.
Reference: Original_Prompts_Precontext_files/full_pipeline_prompt.md
```

---

## Step 1 — OrganizedNotes

### What to do

1. **Ingest** — Copy originals unchanged into `OrganizedNotes/<lecture_id>/source/` as `page_01.jpg`, `page_02.jpg`, etc.
   - PDF sources: convert with `pdftoppm -jpeg -r 200` (or equivalent).

2. **Segment** — Split on graduate-physics semantics (not arbitrary page breaks):

   | Split when you see | `content_type` |
   |--------------------|----------------|
   | Named definition or term | `definition` |
   | Stated result without full proof | `theorem` |
   | Multi-step mathematical argument | `derivation` |
   | Standalone or key displayed equation | `equation` |
   | Sketch, graph, or figure | `diagram` |
   | Worked problem or numeric instance | `example` |
   | Side note, reminder, or aside | `remark` |
   | Illegible or ambiguous content | `unclear` |

3. **Preserve handwriting** — Each block gets `blocks/block_NNN/image.png`; set `handwriting_preserved: true`.

4. **Write metadata** — `manifest.yaml` (lecture level) and `blocks/block_NNN/meta.yaml` (per block).

5. **Validate** before finishing:
   - [ ] Every source page appears in at least one block's `source_ref.page`
   - [ ] `reading_order` in manifest lists every block exactly once
   - [ ] `reading_order` integers in block meta match manifest order
   - [ ] Every block has `image.png` and `meta.yaml`
   - [ ] Low-confidence blocks flagged with `review_notes`, not merged or dropped

### Cursor invocation

```
/physics-notes-organizer
```

Or attach source files and say:

```
Organize these lecture notes into an OrganizedNotes package.
lecture_id: <slug>
course: <course name>
topic: <topic>
date: <YYYY-MM-DD>
conversion_path_hint: direct_latex
```

### Output layout

```
OrganizedNotes/<lecture_id>/
├── manifest.yaml
├── source/
│   ├── page_01.jpg
│   └── ...
└── blocks/
    └── block_NNN/
        ├── image.png
        └── meta.yaml
```

### References

- Schema: `Main_Project/schemas/organized_notes_schema.yaml`
- Cursor skill: `.cursor/skills/physics-notes-organizer/SKILL.md`
- System prompt: `Original_Prompts_Precontext_files/organize_notes_system_prompt.md`
- User template: `Original_Prompts_Precontext_files/organize_notes_user_template.md`
- Minimal example: `Main_Project/examples/sample_lecture/`

---

## Step 3b — Direct LaTeX

### What to do

1. Read `manifest.yaml` — sections, `reading_order`, course/topic/date.
2. Read each `blocks/block_NNN/meta.yaml` in `reading_order`.
3. Use block `image.png` as **authoritative** for symbols and equation layout when attached.
4. Use `ai_summary` and `equations_detected` as **hints only** if they conflict with images.
5. Write one `.tex` file under `OrganizedNotes/<lecture_id>/output/<lecture_id>.tex`.
6. Map `content_type` to LaTeX environments (definition, theorem, derivation + align, equation, remark, includegraphics for diagrams).
7. Add `% block_NNN` before each block; `% REVIEW:` for low/medium confidence.
8. Compile: `pdflatex` twice in the `output/` directory.
9. Write `output/TRIAL_REPORT.md` with blocks covered, flags, compile result.

### User prompt template

```
Using the Step 3b system prompt, convert the OrganizedNotes package below into a single compilable LaTeX file.

Output file: OrganizedNotes/<lecture_id>/output/<lecture_id>.tex
OrganizedNotes path: OrganizedNotes/<lecture_id>/

Include block traceability comments (% block_NNN) and % REVIEW: flags where needed.
Include block images for diagram blocks via \includegraphics.
Compile to PDF and write TRIAL_REPORT.md.
```

### References

- System prompt: `Original_Prompts_Precontext_files/latex_direct_system_prompt.md`
- User template: `Original_Prompts_Precontext_files/latex_direct_user_template.md`

---

## Worked example (validated in this repo)

This is the Test Case we ran end-to-end.

### Source

- **Raw PDF:** `Castillo_Note_files/HC_6001_sample_lectures/Test_Case/Lecture-scattering-Hamiltonian_241022-forward.pdf`
- **Pages:** 4 (scattering + Hamiltonian mechanics)
- **Date on notes:** October 22, 2024

### Step 1 output

- **Package:** `OrganizedNotes/hc6001_2024-10-22_scattering_hamiltonian/`
- **lecture_id:** `hc6001_2024-10-22_scattering_hamiltonian`
- **Blocks:** 17 (`block_001` … `block_017`)
- **Sections:** 12 (central scattering setup → Rutherford cross section → Hamiltonian)

### Step 3b output

- **LaTeX:** `OrganizedNotes/hc6001_2024-10-22_scattering_hamiltonian/output/hc6001_2024-10-22_scattering_hamiltonian.tex`
- **PDF:** `OrganizedNotes/hc6001_2024-10-22_scattering_hamiltonian/output/hc6001_2024-10-22_scattering_hamiltonian.pdf` (7 pages)
- **Report:** `OrganizedNotes/hc6001_2024-10-22_scattering_hamiltonian/output/TRIAL_REPORT.md`

### Block coverage summary

| Section | Blocks |
|---------|--------|
| Central-potential scattering setup | block_001 |
| Differential cross section | block_002 |
| Repulsive vs attractive geometry | block_003 |
| Universal scattering-angle integral | block_004, block_005 |
| Coulomb scattering (general) | block_006, block_007 |
| Coulomb repulsive / attractive | block_008, block_009 |
| Rutherford cross section | block_010, block_011, block_012 |
| Notation, screened potentials | block_013 |
| Hamiltonian intro | block_014 |
| Legendre transformation | block_015 |
| Hamiltonian + canonical equations | block_016, block_017 |

---

## Step 3a — Mathpix (optional alternative)

If `conversion_path_hint: mathpix` in the manifest:

1. Batch OCR each `blocks/block_NNN/image.png` → raw `.tex` per block
2. Merge in `manifest.reading_order`
3. Clean and compile to PDF

Step 3a was **not** run on the worked example above. Use when you want OCR-driven equation transcription rather than agent-written LaTeX from metadata + images.

---

## Quality checklist (full pipeline)

### After Step 1

- [ ] All source pages in `source/` and referenced in block metadata
- [ ] `reading_order` complete and consistent
- [ ] Every block has cropped `image.png` with `handwriting_preserved: true`
- [ ] Unclear content marked `unclear` or `confidence: low` with `review_notes`

### After Step 3b

- [ ] Every block in `reading_order` appears in `.tex` (or `% SKIPPED` with reason)
- [ ] Section headings match `manifest.sections`
- [ ] `% block_NNN` on all blocks
- [ ] `% REVIEW:` on low/medium confidence blocks
- [ ] `pdflatex` succeeds (run twice for references)
- [ ] `TRIAL_REPORT.md` documents coverage and flags

---

## Quick commands

```bash
# Convert PDF pages to JPEG (Step 1 ingest helper)
pdftoppm -jpeg -r 200 SOURCE.pdf OrganizedNotes/<lecture_id>/source/page

# Rename page-01.jpg → page_01.jpg as needed

# Compile Step 3b output
cd OrganizedNotes/<lecture_id>/output
pdflatex <lecture_id>.tex
pdflatex <lecture_id>.tex
```

---

## Related files in this repo

| File | Role |
|------|------|
| `Main_Project/Project_Outline.txt` | High-level project goals |
| `Main_Project/schemas/organized_notes_schema.yaml` | OrganizedNotes schema |
| `Main_Project/examples/sample_lecture/` | Minimal 3-block Step 1 + 3b example |
| `.cursor/skills/physics-notes-organizer/SKILL.md` | Cursor skill for Step 1 |
| `organize_notes_system_prompt.md` | Step 1 system prompt |
| `organize_notes_user_template.md` | Step 1 user template |
| `latex_direct_system_prompt.md` | Step 3b system prompt |
| `latex_direct_user_template.md` | Step 3b user template |
| `Orig_Prompt_Context_file.txt` | Index of prompt files |
