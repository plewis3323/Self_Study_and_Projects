# Create Your Own Higher-Order Functions — Progress Tracker

**Project:** Codecademy MLE Path → Functional Programming → *Create Your Own Higher-Order Functions*
**Work in:** `Higher_Order_Functions_PROJECT.ipynb`
**Started:** 9/24/26

---

## Status: COMPLETE (11/9/26) — Steps 1–10 done, all checks pass; Step 11 (optional) not started

**History:** first attempt (9/24/26) reached ~Step 5, but that code was never saved to the notebook, so the project is starting over.
`solution.py` from Codecademy was pasted 11/9/26 and is NOT copied into the notebook; it's only for a comparison after you finish.

**Concepts covered so far (Q&A 9/24/26):**
- **Iterator** = an *object* that remembers its position in a collection (a bookmark). `next()` moves it
  **forward only**, one item at a time; once used up it stays empty. `iter()` makes one from a list/tuple/etc.
- A **list is iterable but not an iterator**: `next([1,2])` → `TypeError`; `iter([1,2])` fixes it.
- **`filter` / `map` are functions that *return* iterators** (lazy: nothing is checked until `next()` is called).
  `count_filter` is a filter object, not a list/tuple/dict; it walks whatever `iterable` you pass
  (for Step 9 that's the CSV `reader`, so each element is one row = a list of 14 strings).
- **`reduce(func, itr, initial)`**: `x` = accumulator (running count), `y` = current element.
  Step 2 is the loop `acc = 0; for y in count_filter: acc = acc + 1` written as a `reduce`.
  `y` is ignored; the initial value matters (no matches → 0, and avoids `list + 1` on CSV rows).

## Checklist

### Part 1 — `count(predicate, itr)`
- [x] Step 1 — `count_filter = filter(...)`
- [x] Step 2 — `count_reduce = reduce(...)` incrementing by 1 per element, returned
- [x] `check_part1()` passes

### Part 2 — `average(itr)` (recursive)
- [x] Step 3 — `avg_helper(curr_count, itr, curr_sum)` defined inside `average`
- [x] Step 4 — `next_num = next(itr, "null")`, add to sum, bump count
- [x] Step 5 — base case: `"null"` → return the average
- [x] Step 6 — recursive call with updated values, returned
- [x] Step 7 — ordered base case → computation → recursive call
- [x] Step 8 — initial call from `average()` returned
- [x] `check_part2()` passes

### Part 3 — Sales data
- [x] Step 9 — `count_belgiums` via `count()` + `lambda x: x[1] == "Belgium"`
- [x] Step 10 — `avg_portugal` via `average()` + `filter` + `map` + `float()`
- [x] `check_part3()` passes

### Step 11 — Extensions (optional)
- [ ] Other analyses / `median` / `standard_deviation`

## Data
`1kSalesRec.csv` is the real Codecademy file (pasted 9/24/26, validated: 1000 rows, all 14 fields,
revenue/cost/profit arithmetic consistent on every row). Some country names have a trailing space
(`"Mauritius "`, `"Moldova "`, `"Tunisia "`, etc.), which matters only for extensions.

## How we work this project
1. You write the code; ask for a **hint**, a **walkthrough**, or **code** when stuck.
2. Checks are asserts — read the message, it names what's off.
3. On **"done"** → code review, TL;DR, tick this list, commit if asked.

## Results
- Belgium orders: **7**
- Portugal average Total Profit: **632,281.405**

## Bugs hit along the way (11/9/26) — worth remembering
1. Parameter named `iterable` but body used `itr` → `NameError`. Names inside a function must match its parameters.
2. `count` computed `count_reduce` but never returned it → would print `None`.
3. `curr_sum += next_num` placed **before** the base case → would do `float + "null"` → `TypeError`.
   This is why Step 7's order is base case → computation → recursive call.
4. `curr_sum == next_num` (comparison, result thrown away) instead of `curr_sum += next_num`.

## Known limitations (fine for this project)
- `average([])` → `ZeroDivisionError` (count is 0).
- Recursion depth ≈ 1000, so `average()` on all ~1000 rows can hit `RecursionError`.

## Open questions / to verify
- None.
