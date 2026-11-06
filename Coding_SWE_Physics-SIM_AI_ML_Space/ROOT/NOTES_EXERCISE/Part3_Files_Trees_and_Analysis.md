# ROOT Primer, Part 3: Files, Trees & Data Analysis

> **Before this:** [Part 2](Part2_Graphs_Histograms_and_Fitting.md). You should be able to fill, draw, and fit a histogram.
> **Goal:** save objects to `.root` files, store event data in **TTrees**, and analyze them, first with a loop and then the modern way with **RDataFrame**.

---

## 1. ROOT files: `TFile`

A `.root` file is like a **folder of ROOT objects** (histograms, graphs, trees) saved to disk.

### Writing

```cpp
auto f = TFile::Open("my_output.root", "RECREATE");  // RECREATE = overwrite if it exists
auto h = new TH1D("h_mass", "Mass;m [GeV];Events", 100, 0, 10);
// ... fill h ...
h->Write();          // writes it into the open file
f->Close();
```

File modes:

| Mode | Meaning |
|---|---|
| `"READ"` | Read only (the default) |
| `"RECREATE"` | Create the file, **overwriting** it if it exists |
| `"UPDATE"` | Open an existing file and add to it |
| `"NEW"` / `"CREATE"` | Create the file, but fail if it already exists |

### Reading

```cpp
auto f = TFile::Open("my_output.root");
auto h = f->Get<TH1D>("h_mass");   // get the object by its NAME (the first constructor argument)
h->Draw();
```

### Looking inside a file

```bash
root -l my_output.root        # opens ROOT with the file attached as _file0
```
```
root [1] .ls                  // list the contents
root [2] h_mass->Draw()       // objects can be used by name directly
root [3] new TBrowser         // GUI browser (needs a display)
```

From bash, `rootls -l my_output.root` lists the contents without opening ROOT.

---

## 2. Why Trees?

A histogram **throws away** the individual values and keeps only the counts. Real experiments need to keep **every event** with **many variables** (energy, momentum, charge, …), so they can apply new cuts later.

- A **`TTree`** is a table: each **entry** (row) is an **event**, and each **branch** (column) is a **variable**.
- Trees are stored efficiently (compressed, column by column), so they can hold **billions of events**.
- **`TNtuple`** is a simpler tree where every variable is a `float`. It's good for quick work.

---

## 3. Writing a Tree

```cpp
#include "TFile.h"
#include "TTree.h"
#include "TRandom3.h"
#include "TMath.h"

void WriteTree() {
    auto f = TFile::Open("events.root", "RECREATE");
    auto t = new TTree("events", "Toy particle events");

    // 1. variables that hold the values for ONE event
    double px, py, pz, E;
    int    charge;

    // 2. connect each variable to a branch: name, address, "name/type"
    t->Branch("px", &px, "px/D");    // D = double
    t->Branch("py", &py, "py/D");
    t->Branch("pz", &pz, "pz/D");
    t->Branch("E",  &E,  "E/D");
    t->Branch("charge", &charge, "charge/I"); // I = int

    // 3. loop: set the variables, then call Fill() once per event
    TRandom3 rng(1);
    const double m = 0.1396;                  // pion mass [GeV]
    for (int i = 0; i < 100000; ++i) {
        px = rng.Gaus(0, 0.5);
        py = rng.Gaus(0, 0.5);
        pz = rng.Gaus(0, 2.0);
        E  = TMath::Sqrt(px*px + py*py + pz*pz + m*m);
        charge = (rng.Uniform() < 0.5) ? -1 : +1;
        t->Fill();
    }

    t->Write();
    f->Close();
}
```

**The key idea:** `Branch` stores the **address** (`&px`) of your variable. Each `Fill()` copies **whatever is in those variables right now** into a new row.

---

## 4. Quick looks: `TTree::Draw` and `Scan`

Before writing a full analysis, you can explore a tree straight from the prompt:

```
root -l events.root
root [1] events->Print()                       // list the branches
root [2] events->Scan("px:py:charge", "", "", 10)   // first 10 rows as a table
root [3] events->Draw("E")                     // histogram of E
root [4] events->Draw("sqrt(px*px+py*py)")     // you can use formulas: pT
root [5] events->Draw("E", "charge > 0")       // 2nd argument = a CUT
root [6] events->Draw("py:px", "", "COLZ")     // 2D: "y:x"
root [7] events->Draw("E>>hE(100,0,8)")        // fill a named histogram with your own binning
```

This is very useful for checking your data quickly.

---

## 5. Reading a Tree with an event loop

The classic way, which you'll see in lots of existing experiment code:

```cpp
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TMath.h"

void ReadTree() {
    auto f = TFile::Open("events.root");
    auto t = f->Get<TTree>("events");

    double px, py;
    int charge;
    t->SetBranchAddress("px", &px);       // connect branches to your variables
    t->SetBranchAddress("py", &py);
    t->SetBranchAddress("charge", &charge);

    auto hPt = new TH1D("hPt", "p_{T} of positive tracks;p_{T} [GeV];Tracks", 100, 0, 3);

    for (Long64_t i = 0; i < t->GetEntries(); ++i) {
        t->GetEntry(i);                   // loads row i into px, py, charge
        if (charge > 0)
            hPt->Fill(TMath::Sqrt(px*px + py*py));
    }

    auto c = new TCanvas();
    hPt->Draw();
    c->SaveAs("pt_positive.png");
}
```

- **`SetBranchAddress` + `GetEntry(i)`** is the reading version of `Branch` + `Fill()`.
- The **types must match**. Reading a `/D` branch into a `float` gives garbage.

---

## 6. The modern way: `RDataFrame`

**`RDataFrame`** does the same analysis in a few lines, with no manual loop. It's the recommended approach today, and it can run on many CPU cores.

```cpp
#include "ROOT/RDataFrame.hxx"
#include "TCanvas.h"

void AnalyzeRDF() {
    ROOT::RDataFrame df("events", "events.root");     // tree name, file name

    auto hPt = df.Filter("charge > 0")                 // cut
                 .Define("pt", "sqrt(px*px + py*py)")  // new column
                 .Histo1D({"hPt", "p_{T} of positive tracks;p_{T} [GeV];Tracks", 100, 0, 3}, "pt");

    auto nPos = df.Filter("charge > 0").Count();

    auto c = new TCanvas();
    hPt->DrawClone();                                  // the event loop runs HERE, the first time a result is used
    c->SaveAs("pt_rdf.png");
    cout << "Positive tracks: " << *nPos << endl;
}
```

The main ideas:
- **`Filter`** = apply a cut. **`Define`** = make a new column. **`Histo1D` / `Count` / `Mean` / `Snapshot`** = results.
- **Lazy:** nothing runs until you actually *use* a result (`->Draw`, `*nPos`). Then **all** booked results are filled in a **single pass** over the data.
- **`df.Snapshot("newtree", "skim.root", {"px","py","pt"})`** writes a new, smaller tree. This is called **skimming**.
- Multi-threading: put `ROOT::EnableImplicitMT();` before creating the dataframe.

---

## 7. The same thing in Python (PyROOT)

Every ROOT class is also available from Python:

```python
import ROOT

df = ROOT.RDataFrame("events", "events.root")
h = df.Filter("charge > 0").Define("pt", "sqrt(px*px + py*py)") \
      .Histo1D(("hPt", "p_{T};p_{T} [GeV];Tracks", 100, 0, 3), "pt")

c = ROOT.TCanvas()
h.Draw()
c.SaveAs("pt_python.png")

# convert to numpy for matplotlib / ML work
arrays = df.AsNumpy(["px", "py"])
```

- The **strings** in `Filter`/`Define` are still C++. They get compiled, so this runs fast.
- `AsNumpy` is the bridge to pandas, matplotlib, and ML libraries. Outside ROOT, the **`uproot`** package can read `.root` files with pure Python (`pip install uproot`).

---

## 8. Where to go next

- **Official ROOT Primer** (the source for these notes): <https://root.cern/primer/>
- **ROOT tutorials** (hundreds of example macros): <https://root.cern/doc/master/group__Tutorials.html>, also in `$ROOTSYS/tutorials`
- **Class reference** (look up any `T...` class): <https://root.cern/doc/master/>
- **ROOT forum**: <https://root-forum.cern.ch>

---

## ✏️ Exercises: Part 3

1. **Save and reload.** Write a macro that fills two histograms and writes them to `hists.root`. In a **second** macro, open the file, get both histograms, and draw them on the same canvas with a legend.
2. **Explore with `Draw`.** Run `WriteTree.C`, then at the prompt (no macro):
   - Plot the **pseudorapidity** $\eta = -\ln\tan(\theta/2)$, where $\theta = \arctan(p_T / p_z)$. Hint: `TMath::ATan2(pt, pz)` works inside `Draw` strings.
   - How many events have $p_T > 1$ GeV? (`events->GetEntries("sqrt(px*px+py*py) > 1")`)
3. **Add a branch.** Change `WriteTree.C` to also store `pt` as a branch. Check that it's there with `events->Print()`.
4. **Loop vs RDataFrame.** Using `ReadTree.C` and `AnalyzeRDF.C`, confirm that both give the **same number of entries** in `hPt`.
5. **Invariant mass (physics!).** Write a new tree where each event has **two** particles (`px1, py1, pz1, E1, px2, …`). Then with RDataFrame:
   - `Define` the invariant mass $m = \sqrt{(E_1+E_2)^2 - |\vec p_1 + \vec p_2|^2}$
   - Histogram it.
   - **Bonus:** make the two particles come from the decay of a 3 GeV parent (use `TGenPhaseSpace` or a `TLorentzVector` boost) and fit the peak with what you learned in Part 2.
6. **Skim.** Use `Snapshot` to write only events with `charge < 0` and `E > 1` into `skim.root`. How many entries does the new tree have?
7. **PyROOT.** Redo Exercise 4 in a Jupyter notebook using `import ROOT`, then make the $p_T$ plot with matplotlib using `AsNumpy`.

⬅️ [Part 2](Part2_Graphs_Histograms_and_Fitting.md) | 🏠 [ROOT folder](../README.md)
