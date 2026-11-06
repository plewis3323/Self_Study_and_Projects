# ROOT Primer, Part 2: Graphs, Functions, Histograms & Fitting

> **Before this:** [Part 1](Part1_ROOT_Basics_and_Macros.md). You should be able to write and run a macro.
> **Goal:** make the plots physicists make every day: functions, data points with error bars, histograms, and fits.

---

## 0. The pattern you'll see everywhere

Almost every ROOT plot follows the same 4 steps:

```cpp
auto c = new TCanvas("c", "My title", 800, 600);  // 1. a canvas (the window/page)
auto obj = new TH1F(...);                           // 2. make the object (histogram, graph, function)
obj->Draw();                                        // 3. draw it on the current canvas
c->SaveAs("my_plot.png");                           // 4. save it (.png, .pdf, .root, .C …)
```

- **`new` + pointer (`->`)**: ROOT objects are usually made with `new` so they **stay alive after the macro ends** and you can still see the plot. A plain local object (`TH1F h(...)`) is deleted when the function returns, and your plot disappears.
- The **first argument** of most constructors is a **name** (used inside ROOT/files). The **second** is a **title** (shown on the plot).
- **Titles can set axis labels:** `"Main title;x-axis label;y-axis label"`.

> **WSL / no display:** run with `root -l -b -q macro.C` and always `SaveAs(...)`, then open the PNG/PDF from Windows.

---

## 1. Functions: `TF1`

A **`TF1`** is a 1D function you can draw, evaluate, integrate, or fit.

```cpp
// formula as a string, x range 0 to 10
auto f1 = new TF1("f1", "sin(x)/x", 0., 10.);
f1->Draw();

f1->Eval(2.0);        // value at x = 2
f1->Integral(0, 5);   // integral from 0 to 5
f1->GetMaximumX();    // x where the function is largest
```

### Functions with parameters

Parameters are written `[0]`, `[1]`, … in the formula:

```cpp
auto f2 = new TF1("f2", "[0]*x*sin([1]*x)", -3., 3.);
f2->SetParameter(0, 10.);   // [0] = amplitude
f2->SetParameter(1, 5.);    // [1] = frequency
f2->SetParNames("Amp", "Freq");
f2->Draw();
```

**Built-in shortcuts** you'll use constantly: `"gaus"`, `"expo"`, `"pol1"`, `"pol2"`, `"landau"`. For example, `new TF1("g", "gaus", -5, 5)` is a Gaussian with parameters `Constant, Mean, Sigma`.

---

## 2. Data with errors: `TGraphErrors`

Measured data points with error bars:

```cpp
const int n = 5;
double x[n]  = {1, 2, 3, 4, 5};
double y[n]  = {2.1, 3.9, 6.2, 7.8, 10.1};
double ex[n] = {0, 0, 0, 0, 0};          // x errors
double ey[n] = {0.3, 0.3, 0.4, 0.4, 0.5};// y errors

auto gr = new TGraphErrors(n, x, y, ex, ey);
gr->SetTitle("Measurement;x [cm];y [V]");
gr->SetMarkerStyle(20);    // filled circle
gr->SetMarkerColor(kBlue);
gr->Draw("APE");           // A = draw axes, P = points, E = error bars
```

**Draw options** are short strings. The most common for graphs:

| Option | Meaning |
|---|---|
| `A` | Draw the **axes** (needed for the first thing you draw) |
| `P` | **Points** (markers) |
| `L` | **Line** connecting points |
| `E` | **Error** bars |
| `SAME` | Draw on top of what's already there (histograms/functions) |

You can also read data straight from a text file with columns `x y ex ey`:
```cpp
auto gr = new TGraphErrors("data.txt");
```

---

## 3. Fitting

```cpp
auto line = new TF1("line", "[0] + [1]*x", 0, 6);
gr->Fit(line);                      // fits and prints the result
// or simply: gr->Fit("pol1");

double slope    = line->GetParameter(1);
double slopeErr = line->GetParError(1);
double chi2     = line->GetChisquare();
int    ndf      = line->GetNDF();
cout << "slope = " << slope << " +/- " << slopeErr
     << ",  chi2/ndf = " << chi2 << "/" << ndf << endl;
```

What the printout means:
- **Parameter values ± errors**: your best-fit results.
- **χ²/ndf**: goodness of fit. **≈ 1** is good. **≫ 1** means a bad model or underestimated errors. **≪ 1** means the errors are probably overestimated.
- **Starting values matter.** For anything nonlinear (Gaussians, exponentials), call `SetParameter(...)` with a reasonable guess **before** fitting, or the fit may fail.

Show the fit results box on the plot:
```cpp
gStyle->SetOptFit(1111);
```

---

## 4. Histograms: `TH1F`

A **histogram** counts how many values fall in each **bin**. It's the most-used object in particle physics.

```cpp
// name, title, number of bins, low edge, high edge
auto h = new TH1F("h", "Gaussian sample;x;Entries", 50, -5., 5.);

for (int i = 0; i < 10000; ++i)
    h->Fill(gRandom->Gaus(0., 1.));   // random number, mean 0, sigma 1

h->Draw();
h->Fit("gaus");
```

Useful methods:

| Method | Gives you |
|---|---|
| `h->GetEntries()` | Number of times you called `Fill` |
| `h->GetMean()`, `h->GetStdDev()` | Mean and standard deviation of the filled values |
| `h->GetBinContent(i)` | Counts in bin `i` (bins start at **1**. Bin 0 is underflow and bin N+1 is overflow) |
| `h->GetBinCenter(i)` | x position of bin `i` |
| `h->Integral()` | Sum of bin contents |
| `h->Scale(1./h->Integral())` | Normalize to area 1 |

- **`gRandom`** is ROOT's global random number generator. It also has `Uniform(a,b)`, `Exp(tau)`, `Poisson(mu)`, `Landau(...)`, and more.
- **`F` / `D` / `I`** in `TH1F` / `TH1D` / `TH1I` = float / double / int storage. **Prefer `TH1D`** if you're unsure.
- **2D histograms:** `TH2F("h2", "title", nx, xlo, xhi, ny, ylo, yhi)`, then `h2->Fill(x, y)` and `h2->Draw("COLZ")`.

---

## 5. Several plots together

### Overlaying
```cpp
h1->Draw();
h2->SetLineColor(kRed);
h2->Draw("SAME");

auto leg = new TLegend(0.65, 0.7, 0.88, 0.88);  // x1,y1,x2,y2 as fractions of the pad
leg->AddEntry(h1, "Data", "l");
leg->AddEntry(h2, "Simulation", "l");
leg->Draw();
```

### Side by side (pads)
```cpp
auto c = new TCanvas("c", "two plots", 1200, 500);
c->Divide(2, 1);          // 2 columns, 1 row
c->cd(1); h1->Draw();     // go to pad 1
c->cd(2); gr->Draw("APE");// go to pad 2
c->SaveAs("side_by_side.png");
```

### Log scale
```cpp
c->SetLogy();   // log y axis (common for spectra)
```

---

## 6. Complete example macro

`FitDemo.C`: fill a histogram, fit it, save the plot.

```cpp
#include "TCanvas.h"
#include "TH1D.h"
#include "TF1.h"
#include "TRandom3.h"
#include "TStyle.h"

void FitDemo() {
    gStyle->SetOptFit(1111);
    TRandom3 rng(42);                       // fixed seed, so you get the same result every run

    auto h = new TH1D("h", "Signal on background;Mass [GeV];Events", 100, 0., 10.);
    for (int i = 0; i < 5000; ++i) h->Fill(rng.Exp(3.));      // falling background
    for (int i = 0; i < 1000; ++i) h->Fill(rng.Gaus(5., 0.3)); // a peak at 5 GeV

    auto f = new TF1("f", "expo(0) + gaus(2)", 0., 10.);       // expo uses [0],[1] and gaus uses [2],[3],[4]
    f->SetParameters(5., -0.3, 130., 5., 0.3);                  // starting guesses
    h->Fit(f, "R");                                             // R = fit only in the function's range

    auto c = new TCanvas("c", "fit", 800, 600);
    h->Draw("E");
    c->SaveAs("FitDemo.png");
}
```

Run it: `root -l -b -q FitDemo.C`, then open `FitDemo.png`.

---

## ✏️ Exercises: Part 2

1. **Draw a function.** Plot $f(x) = e^{-x/2}\cos(3x)$ for $0 \le x \le 10$. Save it as a PNG. Find the integral from 0 to 10 with `Integral`.
2. **Parameters.** Make a `TF1` for a damped oscillator $A e^{-x/\tau}\cos(\omega x)$ with 3 parameters. Draw 3 versions with different τ on the **same** canvas in different colors, and add a legend.
3. **Ohm's law fit.** Make a `TGraphErrors` with current $I$ = 0.1…0.5 A and voltage $V$ = 1.1, 2.0, 3.1, 3.9, 5.2 V (σ_V = 0.2 V). Fit `pol1`.
   - What is the resistance ± its error?
   - Is the intercept consistent with 0?
   - What is χ²/ndf?
4. **Histogram stats.** Fill a `TH1D` with 10⁴ values from `gRandom->Uniform(0, 1)`.
   - Compare `GetMean()` and `GetStdDev()` with the exact values (1/2 and $1/\sqrt{12}$).
   - Repeat with 10² entries. What changes?
5. **Central limit theorem.** Fill a histogram where each entry is the **sum of 12 uniform random numbers minus 6**. Fit it with `gaus`. What mean and σ do you get? Why?
6. **Peak finding.** Change `FitDemo.C`:
   - Move the peak to 2 GeV, where the background is larger. Does the fit still find it?
   - Make the peak 10× smaller. When does the fit stop being reliable?
   - Plot with `c->SetLogy()`.
7. **2D histogram.** Fill a `TH2D` with $(x, y)$ where both are Gaussian, but $y = 0.8x + 0.6\,\cdot$`Gaus(0,1)`. Draw it with `"COLZ"`. Then try `h2->ProjectionX()->Draw()`.

⬅️ [Part 1](Part1_ROOT_Basics_and_Macros.md) | ➡️ **Next:** [Part 3: Files, Trees & Data Analysis](Part3_Files_Trees_and_Analysis.md)
