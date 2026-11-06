# ROOT

ROOT (CERN data-analysis framework) practice: macros, histograms, fits, TTrees.

## NOTES_EXERCISE: ROOT Primer for beginners (3 parts)

A first look at ROOT, based on the official [ROOT Primer](https://root.cern/primer/). Work through the parts in order. Each one ends with exercises, and you can save your exercise macros (`ex1_1.C`, …) in the same folder.

| Part | Topics |
|---|---|
| [Part 1: Basics & Macros](NOTES_EXERCISE/Part1_ROOT_Basics_and_Macros.md) | The prompt (Cling), `TMath`, C++ at the prompt, writing/running/compiling macros |
| [Part 2: Graphs, Histograms & Fitting](NOTES_EXERCISE/Part2_Graphs_Histograms_and_Fitting.md) | `TCanvas`, `TF1`, `TGraphErrors`, `TH1`/`TH2`, fitting and χ², legends, pads |
| [Part 3: Files, Trees & Analysis](NOTES_EXERCISE/Part3_Files_Trees_and_Analysis.md) | `TFile`, writing/reading `TTree`s, `TTree::Draw`, `RDataFrame`, PyROOT |

Run macros with `root -l -b -q Macro.C` (batch mode, which works in WSL) and save plots with `SaveAs`.
Earlier practice files are in `../Misc/ROOT/` (the original partial `ROOT_Primer.C` is in `../Misc/ROOT/Tutorials/`).
