# Summer-26-Dr.-Castillo-AI-TA-Task

Use AI (chatbots and agentic workflows) to convert graduate-level physics handwritten lecture notes into readable, reproducible LaTeX-PDF outputs for the Ohio University Physics Department.

## Pipeline

| Step | Description |
|------|-------------|
| **0** | Raw notes — paper, whiteboard, scans (disorganized or not) |
| **1** | **OrganizedNotes** — AI-readable structure with segmented handwriting blocks |
| **3a** | Mathpix OCR on block images → raw LaTeX → PDF |
| **3b** | Direct LaTeX agent using manifest + block metadata + images → PDF |

Step 1 and Step 3b prompts are implemented. Step 3a (Mathpix) is documented for downstream handoff.

**Full pipeline (Step 1 → Step 3b):** [full_pipeline_prompt.md](Original_Prompts_Precontext_files/full_pipeline_prompt.md)

## Quick start (Step 1)

**In Cursor:** The agent skill [`.cursor/skills/physics-notes-organizer/SKILL.md`](.cursor/skills/physics-notes-organizer/SKILL.md) guides segmentation and metadata generation.

**Manual prompts:**

- [organize_notes_system_prompt.md](Original_Prompts_Precontext_files/organize_notes_system_prompt.md)
- [organize_notes_user_template.md](Original_Prompts_Precontext_files/organize_notes_user_template.md)

**Schema and example:**

- [organized_notes_schema.yaml](Main_Project/schemas/organized_notes_schema.yaml)
- [sample_lecture/](Main_Project/examples/sample_lecture/)

**Output directory:** Place organized packages in [`OrganizedNotes/`](OrganizedNotes/).

## Step 3b — Direct LaTeX (try it)

**Prompts:**

- [latex_direct_system_prompt.md](Original_Prompts_Precontext_files/latex_direct_system_prompt.md)
- [latex_direct_user_template.md](Original_Prompts_Precontext_files/latex_direct_user_template.md)

**Trial run on sample lecture:**

- Input: [sample_lecture/](Main_Project/examples/sample_lecture/)
- Output: [sample_lecture_lagrangian.tex](Main_Project/examples/sample_lecture/output/sample_lecture_lagrangian.tex)
- Report: [TRIAL_REPORT.md](Main_Project/examples/sample_lecture/output/TRIAL_REPORT.md)

**Full Test Case run (17 blocks, scattering + Hamiltonian):**

- Input: [Test_Case PDF](Castillo_Note_files/HC_6001_sample_lectures/Test_Case/Lecture-scattering-Hamiltonian_241022-forward.pdf)
- OrganizedNotes: [hc6001_2024-10-22_scattering_hamiltonian/](OrganizedNotes/hc6001_2024-10-22_scattering_hamiltonian/)
- Output: [tex](OrganizedNotes/hc6001_2024-10-22_scattering_hamiltonian/output/hc6001_2024-10-22_scattering_hamiltonian.tex) · [TRIAL_REPORT.md](OrganizedNotes/hc6001_2024-10-22_scattering_hamiltonian/output/TRIAL_REPORT.md)

## Project docs

- [Project_Outline.txt](Main_Project/Project_Outline.txt)
- [Original ChatGPT context](Original_Prompts_Precontext_files/Orig_Prompt_Context_file.txt)
