# sPHENIX Software & Experiment Learning Space and Notes

Working space for learning sPHENIX software (Fun4All, simulations, analysis) and notes on the experiment.

## Self-paced sPHENIX course (built from the Summer-2026 sPHENIX School)

A self-paced course in ten modules plus a syllabus. It is built from my notes on the
**Summer-2026 sPHENIX School and Workfest** (BNL, 27 Jul – 14 Aug 2026) and the public sPHENIX literature.
Each module is **self-contained**. It starts from first principles and works up to how sPHENIX actually
does things, with short derivations, worked (toy) numbers, "Connect" boxes that link the material to my own
analyses (Au+Au π0 R_CP, π0 efficiency simulation, tower-slope calibration, p+p Run-24 π0/η cross section),
self-test questions with answers, and a glossary. The SDCC exercises are optional.

Start with the syllabus, then read the modules in order. Modules 3–5 can be read in any order;
Module 6 comes before 7 and 8.

| # | File | Topic | Week | Pages |
|---|------|-------|------|-------|
| — | [00_Syllabus.pdf](00_Syllabus.pdf) | Syllabus: 12-week plan, module scopes, dependencies, list of school talks [S01]-[S50] | — | 7 |
| 1 | [Module01_Physics_Program.pdf](Module01_Physics_Program.pdf) | The sPHENIX physics program: QGP, jet quenching, heavy flavor, cold QCD and spin | 1 | 22 |
| 2 | [Module02_RHIC_and_Detector_Overview.pdf](Module02_RHIC_and_Detector_Overview.pdf) | RHIC and the sPHENIX detector: beams, layout, coordinates, MBD/ZDC/sEPD, runs, centrality and event plane | 2 | 20 |
| 3 | [Module03_Calorimeters.pdf](Module03_Calorimeters.pdf) | Calorimetry: EM and hadronic showers, EMCal and inner/outer HCal hardware, resolution, calibration strategy | 3 | 28 |
| 4 | [Module04_Tracking_Detectors.pdf](Module04_Tracking_Detectors.pdf) | Tracking detectors: MVTX, INTT, TPC and TPOT — sensing, readout and their roles in tracking | 4 | 23 |
| 5 | [Module05_Trigger_DAQ_Streaming.pdf](Module05_Trigger_DAQ_Streaming.pdf) | Trigger, DAQ and streaming readout: GL1, triggered vs streaming, raw data to DSTs, computing access | 5 | 22 |
| 6 | [Module06_Fun4All_and_Simulation.pdf](Module06_Fun4All_and_Simulation.pdf) | Fun4All framework, software stack and simulation: SubsysReco, nodes, CDB, generators, Geant4, embedding | 6–7 | 30 |
| 7 | [Module07_Calorimeter_Reconstruction.pdf](Module07_Calorimeter_Reconstruction.pdf) | Calorimeter reconstruction and calibration: waveforms to towers, π0 and tower-slope calibration, clustering, photons, jets | 8 | 24 |
| 8 | [Module08_Tracking_Reconstruction.pdf](Module08_Tracking_Reconstruction.pdf) | Tracking reconstruction: momentum measurement, clustering, seeding, Kalman-filter fitting, vertexing, alignment, TPC distortions, track–calorimeter matching | 9 | 22 |
| 9 | [Module09_Analysis_Workflow.pdf](Module09_Analysis_Workflow.pdf) | From data to a result: run QA, triggers, luminosity, centrality, efficiency, unfolding, systematics, PPG/IRC path | 10 | 24 |
| 10 | [Module10_Case_Studies_and_ML.pdf](Module10_Case_Studies_and_ML.pdf) | Case studies from the 2026 school and machine learning in sPHENIX | 11–12 | 21 |

About 96 hours in total over 12 weeks (8–10 h per week).

### Sources and content policy
- School talks are **paraphrased**, not reproduced, and cited as `[S01]`–`[S50]` (the full list is in the syllabus).
  The talks themselves are on the collaboration-protected Indico event and are not in this repository.
- No slide figures are reproduced. All figures are schematic TikZ drawings made for these notes.
- Only public numbers appear: design values, published sPHENIX papers, PDG and textbook values.
  Internal or preliminary results are described qualitatively, and illustrative numbers are labelled as toy values.
- Software class and macro names were checked against `coresoftware` at the time of writing. Where a name was
  not checked, the text says so; check the current source before relying on it.

### My reading notes
Q&A notes taken while reading the modules are in [`Notes/`](Notes/):
- Module 6: [Module06_Notes.md](Notes/Module06_Notes.md) ([PDF](Notes/Module06_Notes.pdf))

The PDFs are built with pandoc:
`pandoc Module06_Notes.md -o Module06_Notes.pdf --pdf-engine=xelatex -V geometry:margin=2cm -V mainfont="DejaVu Sans" -V monofont="DejaVu Sans Mono"`

### Rebuilding the PDFs
The LaTeX sources are in [`tex/`](tex/). Each file builds on its own with `pdflatex` (run it twice for the
table of contents). It uses only packages available in TeX Live 2020 on SDCC:

```bash
cd tex && pdflatex Module01_Physics_Program.tex && pdflatex Module01_Physics_Program.tex
```

Author: Parker D. Lewis (Ohio University, sPHENIX).
