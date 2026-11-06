# ROOT Primer, Part 1: The Prompt, C++ in ROOT, and Macros

> **Who this is for:** your first time using ROOT. You only need basic C++ (variables, `for` loops, functions).
> **Source:** based on the official [ROOT Primer](https://root.cern/primer/), rewritten as study notes.
> **Time:** ~1–2 sessions. Do the exercises at the bottom before you move on to Part 2.

---

## 1. What is ROOT?

- ROOT is CERN's **data-analysis framework**. It's a big C++ library for histograms, fitting, plotting, and storing large amounts of event data in files.
- Almost every particle/nuclear physics experiment (ATLAS, CMS, ALICE, sPHENIX, …) stores its data in ROOT files.
- You can use it in three ways:
  1. **Interactive prompt**: type C++ and get the result right away (like a calculator).
  2. **Macros**: `.C` files of C++ that ROOT runs for you (these are your scripts).
  3. **Python (PyROOT)**: the same classes from Python (`import ROOT`).

### Key vocabulary

| Term | Meaning |
|---|---|
| **Cling** | The C++ interpreter inside ROOT. It runs C++ line by line, with no separate compile step. |
| **Macro** | A `.C` file with C++ code that ROOT runs. |
| **Namespace** | A named container for functions/classes so names don't clash, e.g. `TMath::Pi()`. |
| **`T` prefix** | Almost every ROOT class starts with `T`: `TH1F`, `TF1`, `TCanvas`, `TFile`… |
| **STL** | The C++ Standard Library (`std::vector`, `std::sort`, …). Cling understands it all. |

---

## 2. Starting and quitting ROOT

```bash
root          # start the interactive prompt
root -l       # start without the splash screen (use this one)
root -l -b    # "batch" mode: no graphics windows (good for servers/WSL)
```

Inside ROOT:

```
.q            // quit
.?            // list of the "dot" commands
.help         // same
```

> **Dot commands** (`.q`, `.x`, `.L`) are ROOT commands, not C++. They always start with a `.`.

---

## 3. ROOT as a calculator

```cpp
root [0] 1+1
(int) 2
root [1] 2*(4+2)/12.
(double) 1.000000
root [2] sqrt(3.)
(double) 1.732051
root [3] 1 > 2
(bool) false
root [4] TMath::Pi()
(double) 3.141593
root [5] TMath::Erf(.2)
(double) 0.222703
```

What to notice:
- ROOT prints the **type** and the **value** of every expression.
- `2*(4+2)/12.` gives a `double` because of the `.` after `12`. Without it, `2*(4+2)/12` is integer division.
- Physics/math functions live in the **`TMath` namespace**: `TMath::Pi()`, `TMath::Exp()`, `TMath::Gaus()`, `TMath::Power()`, `TMath::Abs()`, …

---

## 4. Variables and loops at the prompt

Example: check the geometric series formula
$\sum_{i=0}^{N-1} x^i = \frac{1-x^N}{1-x}$

```cpp
root [0] double x = .5
root [1] int N = 30
root [2] double geom_series = 0
root [3] for (int i = 0; i < N; i++) geom_series += TMath::Power(x, i)
root [4] cout << TMath::Abs(geom_series - (1 - TMath::Power(x, N)) / (1 - x)) << endl;
0
```

What to notice:
- You can declare variables and write loops just like in a normal C++ program.
- **The `;` is optional at the prompt.** Without `;`, ROOT prints the result. With `;`, it stays quiet.
- `cout`/`endl` work without `std::` or `#include`, because ROOT loads them for you.

> **Note:** the original primer writes `TMath::Power(x, N-1)`. That version differs from the sum by about 1.86e-9 and is a small typo. With `N` the two sides match exactly.

---

## 5. Real C++ at the prompt (lambdas, vectors, sorting)

Cling is built on **LLVM/Clang** (a real compiler toolkit), so modern C++ works:

```cpp
root [0] using doubles = std::vector<double>;
root [1] auto pVec = [](const doubles& v){ for (auto&& x : v) cout << x << endl; };
root [2] doubles v{0, 3, 5, 4, 1, 2};
root [3] pVec(v);
root [4] std::sort(v.begin(), v.end());
root [5] pVec(v);
root [6] std::sort(v.begin(), v.end(), [](double a, double b){ return a > b; });
root [7] pVec(v);
```

- `auto pVec = [](...){...}` is a **lambda**, a small unnamed function stored in a variable.
- `std::sort` with a third argument lets you choose the sort order (here, descending).
- This makes the prompt a good place to **practice plain C++** too.

---

## 6. Macros: saving your work in a file

Typing at the prompt is fine for quick tests. For anything real, write a **macro**.

### Rule: the function name matches the file name

`MacroName.C`:
```cpp
void MacroName() {
    // your code here
    cout << "Hello from a macro!" << endl;
}
```

### Running a macro

| How | What it does |
|---|---|
| `root -l MacroName.C` | Start ROOT and run it |
| `root -l -b -q MacroName.C` | Run it with no graphics, then quit (`-q`). Good for scripts. |
| `.x MacroName.C` | Run it from inside ROOT |
| `.L MacroName.C` then `MacroName()` | **Load** it first, then call the function yourself |

### Passing arguments

```cpp
// Square.C
void Square(double x = 2.0) {
    cout << x << "^2 = " << x*x << endl;
}
```
```bash
root -l -b -q 'Square.C(7)'      # note the quotes around the argument
```

### Compiling a macro (faster and catches more errors)

```
root [0] .L MacroName.C+     // the "+" compiles it with ACLiC
root [1] MacroName()
```

- A trailing `+` compiles the macro into a shared library, so it **runs much faster** and the compiler **catches more mistakes**.
- To compile a macro, you need the proper `#include`s (e.g. `#include "TMath.h"`, `#include <iostream>`). Get into the habit of always adding them.

---

## 7. Style tips for beginners

- Put **`#include`s at the top** of every macro, even though the interpreter doesn't need them. Then the macro also compiles with `+`.
- Use **`root -l`** so you skip the splash screen.
- In **WSL** with no display, use `-b`. Save plots with `canvas->SaveAs("plot.png")` instead of looking at a window (Part 2 covers this).
- Use `Tab` to auto-complete class and method names at the prompt: type `TMath::` then press `Tab`.

---

## ✏️ Exercises: Part 1

> Save your exercise macros next to this file, e.g. `ex1_1.C`, `ex1_2.C`, …

1. **Calculator warm-up.** At the prompt, compute:
   - `7/2` and `7/2.`. Why are the answers different?
   - $e^{-1}$ with `TMath::Exp`
   - The value of a Gaussian at $x = 1$ with mean 0 and σ = 1 (`TMath::Gaus`). Then try the normalized version: look up the extra argument.
2. **Semicolons.** Type `double y = 3.0` with and without `;`. What changes in the output?
3. **Geometric series macro.** Turn Section 4 into a macro `GeomSeries.C` that takes `x` and `N` as arguments and prints both the loop sum and the formula.
   - Run it as `root -l -b -q 'GeomSeries.C(0.9, 100)'`.
   - What happens for `x = 1`? Why?
4. **Lambdas and vectors.** Write a macro that fills a `std::vector<double>` with the squares of 1–10 and prints only the even ones (use a lambda).
5. **Interpreted vs compiled.** Write `SlowLoop.C`, which sums `TMath::Sqrt(i)` for `i` from 0 to 10⁸.
   - Time `.x SlowLoop.C` vs `.x SlowLoop.C+` (use `TStopwatch` or the `time` command in bash).
   - Which is faster? What did you need to `#include` for the `+` version to work?
6. **Explore.** At the prompt, type `TMath::` and press `Tab`. Pick 3 functions you didn't know and write one line on what each one does.

➡️ **Next:** [Part 2: Graphs, Functions, Histograms & Fitting](Part2_Graphs_Histograms_and_Fitting.md)
