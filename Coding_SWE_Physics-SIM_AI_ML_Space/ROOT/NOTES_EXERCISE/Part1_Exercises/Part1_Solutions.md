# Part 1 Exercises: Solutions and Answers

Tested on ROOT 6.36.14 (snap, WSL2). Every macro runs both **interpreted** (`root -l -b -q X.C`)
and **compiled with ACLiC** (`root -l -b -q X.C+`). All of them include their headers, so they compile.

| Exercise | Macro |
|---|---|
| 1. Calculator warm-up | [`Calculator.C`](Calculator.C) |
| 2. Semicolons | prompt only (see below) |
| 3. Geometric series | [`GeomSeries.C`](GeomSeries.C) |
| 4. Lambdas and vectors | [`EvenSquares.C`](EvenSquares.C) |
| 5. Interpreted vs compiled | [`SlowLoop.C`](SlowLoop.C) |
| 6. Explore `TMath::` | [`Explore.C`](Explore.C) |

---

## 1. Calculator warm-up

```
7/2   = 3          (int / int -> int, truncated)
7/2.  = 3.5        (int / double -> double)
exp(-1) = 0.367879
Gaus(1,0,1)        = 0.606531   peak height 1: exp(-x^2/2)
Gaus(1,0,1,kTRUE)  = 0.241971   normalized: divided by sqrt(2*pi)*sigma
```

- **Why do `7/2` and `7/2.` differ?** If both operands are `int`, C++ does integer division and drops the fractional part. `2.` is a `double`, so `7` is promoted and you get `3.5`.
- **The extra argument:** `TMath::Gaus(x, mean, sigma, norm)`. When `norm = false` (the default), the peak height is 1. When `norm = true`, the integral is 1. Check: 0.606531 / √(2π) = 0.241971.

## 2. Semicolons

```
root [0] double y = 3.0
(double) 3.0000000
root [1] double z = 3.0;
root [2]
```

Without the `;`, ROOT prints the type and value. With the `;`, it prints nothing. Inside a macro file you **must** use `;` because it is ordinary C++.

## 3. Geometric series

```
root -l -b -q 'GeomSeries.C(0.5, 30)'   ->  loop = 2,        formula = 2,        |diff| = 0
root -l -b -q 'GeomSeries.C(0.9, 100)'  ->  loop = 9.99973,  formula = 9.99973,  |diff| = 5.3e-15
root -l -b -q 'GeomSeries.C(1.0, 10)'   ->  loop = 10,       formula = -nan
```

- **x = 1:** the formula becomes (1 − 1)/(1 − 1) = 0/0, and in floating point that is `NaN`. The loop still works: it adds 1 ten times, so the answer is N. The formula is only valid for x ≠ 1. (The limit as x → 1 is N, by L'Hôpital's rule.)
- The tiny 5e-15 difference at x = 0.9 is floating-point rounding, not a bug.

## 4. Lambdas and vectors

```
Even squares of 1-10: 4 16 36 64 100
```

The lambda `[](double v){ return (long)v % 2 == 0; }` decides which values to print. `%` only works on integers, so the `double` is cast first.

## 5. Interpreted vs compiled

Sum of √i for i = 0 … 10⁸ = 6.66667e+11 (check: ∫₀ᴺ √x dx = ⅔N^{3/2} = 6.67e11 ✓)

| Mode | Real time |
|---|---|
| `.x SlowLoop.C` (interpreted) | ~0.32 s |
| `.x SlowLoop.C+` (ACLiC compiled) | ~0.20 s |

- **Compiled is faster**, but only by about 1.6× here. Modern Cling **JIT-compiles** every function before running it, so a simple loop like this one already runs as machine code. The gap is much bigger in older ROOT (5) and for code that does more work at the top level of the prompt. ACLiC also optimizes more aggressively.
- **Includes needed for `+`:** `<iostream>` (for `std::cout`), `"TMath.h"`, and `"TStopwatch.h"`. You also have to write `std::cout` (or add `using namespace std;`). The interpreter forgives these mistakes, but the real compiler does not.
- 10⁸ still fits in an `int`, but I used `long i` and `100000000L` so the loop is safe if you raise the limit. The sum has to be a `double`, because it is far larger than any `int` can hold.
- ACLiC writes `SlowLoop_C.so`, `.d`, and `.pcm` files next to the macro. They are listed in `.gitignore`.

## 6. Explore `TMath::`

```
TMath::Binomial(5, 2)     = 10        "n choose k": the number of ways to pick k items from n
TMath::Prob(10.0, 10)     = 0.440493  the p-value for chi2 = 10 with ndf = 10, i.e. how likely a chi2 at least this big is by chance
TMath::BreitWigner(0,0,1) = 0.63662   the Breit-Wigner (Cauchy) resonance line shape; peak = 2/(pi*Gamma)
```

`TMath::Prob` is the one you will use most. It turns a fit's χ²/ndf into a goodness-of-fit probability (Part 2, fitting).
