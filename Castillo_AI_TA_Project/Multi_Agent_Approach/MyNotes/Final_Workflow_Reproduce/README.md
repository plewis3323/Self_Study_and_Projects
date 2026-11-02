# Feed `Multi_Agent_Outline.md` to an agent. That is the whole process.

This directory is everything a colleague needs to run this pipeline
themselves, from zero, on their own lecture material. The process is not a
script you invoke — it is a markdown specification you hand to an AI coding
agent, and the agent does the work: segmenting the source PDF, running
independent reviewer sub-agents, transcribing to tagged LaTeX, and auditing
the result for accessibility until every gate closes.

## Do this, in order

1. **Read `Directory_Creation.pdf`** and create the folders it describes
   before you do anything else. The agent expects a specific layout; giving
   it an empty project root with the right folder names is the fastest path
   to a clean run.
2. **Read `Installation.pdf`** and install the toolchain (`Installation/install_toolchain.sh`
   does the heavy lifting). Do this before starting the agent — a probe step
   early in `Multi_Agent_Outline.md` will catch a bad toolchain, but fixing
   it *after* the agent has started costs you a restart.
3. **Put one handwritten/board PDF per lecture into `Input/`** (the folder
   you created in step 1). `Example_Input_Directory/` shows exactly what
   this looks like with a real lecture.
4. **Open this whole folder in an agent platform that can run commands,
   write files, and see images on this machine** — Cursor Agent, Claude
   Code, or Codex CLI. A browser chat window cannot run this; it needs to
   execute shell commands and read/write your filesystem.
5. **Attach or open `Multi_Agent_Outline.md` and send it to the agent.**
   That file is both the kickoff message and the full specification. Do not
   paste a second prompt or summarize it — the agent reads its own
   instructions and begins at Stage 0.
6. The agent will render pages, segment them, run 3 independent reviewer
   sub-agents on the segments, assemble an approved PDF, choose a reference
   textbook, transcribe to accessible tagged LaTeX, run 5 physics referees
   plus an Accessibility Auditor, and hand you a finished package — by
   default in a folder named `Final_Product_Ready/` plus a `For<Recipient>/`
   hand-off package. Expect it to take a while and to loop through several
   review rounds; that looping is the point, not a malfunction.

## What is in this folder

| Item | What it is |
|---|---|
| `Multi_Agent_Outline.md` | **The kickoff file.** Full pipeline specification: operating principles, every stage, every accessibility requirement, the command reference. This is what you send to the agent. |
| `Directory_Creation.pdf` | What folders to create before you start, and why the layout matters. |
| `Installation.pdf` + `Installation/install_toolchain.sh` + `Installation/requirements.txt` | What toolchain the pipeline needs and how to install it. The `.sh` does the install; the PDF explains what it does and why the usual shortcuts (system LaTeX, PyMuPDF instead of poppler) silently fail instead of erroring. |
| `Reproduce.pdf` | How to verify the toolchain and this kit are working *before* trusting them with real material, and what each verification command actually proves. |
| `Accessibility_Info.pdf` | What accessibility standard this pipeline targets, why, and how conformance is actually verified (a checker passing is not the evidence — see the PDF). |
| `Example_Input_Directory/` | A real completed example of what goes in `Input/`: one source lecture PDF. |
| `Example_Intermediate_Directory/` | The same run's Stage 1–3 output: segmented PNGs, `segment_manifest.json`, the Stage 2 review log, and the assembled pre-LaTeX PDF Stage 4 transcribes from. This is what the manifest and review-log requirements in Stages 1–3 look like filled in. |
| `Example_Deliverable_Directory/` | A real completed example of what the agent produces: the tagged PDF, its LaTeX source, figures, HTML/MathML companion, `MANIFEST.json`, and the full accessibility evidence (veraPDF, the four Step 4d numeric tests, and the real PAC 2026 reports this pipeline's own accessibility rulings were built from) — all the way through six rounds of physics review plus the PAC-driven fixes narrated in `PIPELINE_LOG.md`. |
| `style/goldsteinnotes.sty` | The shared, subject-editable preamble the pipeline's LaTeX documents build on. Read its own comments before editing — it deliberately binds no physical quantity to a letter. |
| `tools/` | Every reusable script the pipeline calls by name: segmentation, coverage checking, structure/contrast/accessibility verification, and the post-build PDF tagging fixes. `Multi_Agent_Outline.md`'s own Command Reference explains what each one does and when it runs. |
| `refs/OU-accessibility-sources/` | The actual source PDFs (plus `sources.md` citing them) behind the Governing Standard section's worked Ohio University profile — the DOJ rule, OHIO's OIT guidelines, the 7 Core Skills, the faculty checklist. Replace this folder with your own institution's equivalents when porting the pipeline; see the Appendix in `Multi_Agent_Outline.md` for how. |
| `PIPELINE_LOG.md` | The narrative build log this kit's hard-won rules were distilled from — every dead end, every checker that lied, every fix, in the order they actually happened. `Multi_Agent_Outline.md` and the accessibility evidence cite specific entries by name; this is where those citations resolve. |
| `Final_Workflow_Reproduce.zip` | This entire folder, zipped, as of the last update to `Multi_Agent_Outline.md` — hand this single file to a colleague instead of copying the directory by hand. Re-zip it after any edit; it is not kept in sync automatically. |

## If something looks wrong

Read `Accessibility_Info.pdf` before assuming a clean checker run means the
document is actually accessible — it is not the same claim, and this
pipeline exists partly because that gap is easy to miss. If the agent's
output disagrees with what `Example_Deliverable_Directory/` shows for a
comparable lecture, that is worth a second look before shipping.
