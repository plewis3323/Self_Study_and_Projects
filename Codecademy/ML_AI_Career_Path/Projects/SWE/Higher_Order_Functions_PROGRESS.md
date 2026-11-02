# Create Your Own Higher-Order Functions — Progress Tracker

**Project:** Codecademy MLE Path → Functional Programming → *Create Your Own Higher-Order Functions*
**Work in:** `Higher_Order_Functions_PROJECT.ipynb`
**Started:** 9/24/26

---

## Status: PAUSED (9/24/26) — no code written yet; resume at Step 1/2

**Where you left off:** understood what Steps 1–2 ask; next is writing `count()` in the notebook.

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
- [ ] Step 1 — `count_filter = filter(...)`
- [ ] Step 2 — `count_reduce = reduce(...)` incrementing by 1 per element, returned
- [ ] `check_part1()` passes

### Part 2 — `average(itr)` (recursive)
- [ ] Step 3 — `avg_helper(curr_count, itr, curr_sum)` defined inside `average`
- [ ] Step 4 — `next_num = next(itr, "null")`, add to sum, bump count
- [ ] Step 5 — base case: `"null"` → return the average
- [ ] Step 6 — recursive call with updated values, returned
- [ ] Step 7 — ordered base case → computation → recursive call
- [ ] Step 8 — initial call from `average()` returned
- [ ] `check_part2()` passes

### Part 3 — Sales data
- [ ] Step 9 — `count_belgiums` via `count()` + `lambda x: x[1] == "Belgium"`
- [ ] Step 10 — `avg_portugal` via `average()` + `filter` + `map` + `float()`
- [ ] `check_part3()` passes

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

## Open questions / to verify
- None yet.
