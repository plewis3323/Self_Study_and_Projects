# Functional Programming in Python — Progress Tracker

**Lesson:** Codecademy MLE Path → SWE for ML → *Functional Programming*
**Note file:** `Functional_Programming_Python_Lesson.ipynb`
**Started:** 8/21/26
**Prereqs:** `OOP_Python_Lesson.ipynb` (Introduction to Classes) — COMPLETE 8/12/26; `OOP_Python_Part2_Lesson.ipynb` (Four Pillars) — COMPLETE 8/18/26

---

## Status: COMPLETE — all 10 sublessons folded in, finished 9/23/26
TL;DR written, header scope line replaced with the real topic list. Not committed.
Notebook runs top-to-bottom clean (`nbconvert --execute --inplace`, exit 0, 31 code cells, no error outputs, 9/23/26). Verified outputs on the stand-in data files: zillow lesson code → 5 `house` records; houses after 1985 → indexes **2, 4**, most expensive → **index 2, 185000**; trees checkpoint → 5 `tree` records; height > 75 → only tree 5, `widest` → **index 5, width 10.7**; cities lesson code → 7 `city` records; `asia` → **Tokyo, Mumbai, Bangkok**, `west` → **Mumbai (72.88)**. Earlier verified outputs: `scott.name` / `scott.age` / `scott.grade` → **Scott** / **28** / **A**; `students[1].name` → **Nicole**; `total_cost` with named `rect`/`tri` → **75** / **84.0**; same with inline lambdas → **75** / **84.0**; variable-stored lambdas → **25 21.0**; `odd_or_even(5, cube, square)` → **25**; `filter` imperative → **[2, 4, 6, 8, 10]** and declarative → **(2, 4, 6, 8, 10)**; `map` both ways → **(1, 4, 9, 16, 25, 36, 49, 64, 81, 100)**; `reduce` sum both ways → **37**.

## Sublesson checklist
Mark `[x]` when the summary + any Q/A + code exercise are folded into the notebook **from the real source**.

- [x] **Immutable Data Types** (immutability → thread-safe manipulation + no accidental value changes; tuple-of-tuples is positional and error-prone; `collections.namedtuple` gives named fields on an immutable tuple subclass; convention is subclass name == variable name) + code (`student = namedtuple(...)`; `scott`/`nicole`/`john`; field access; packed into `students`) + real checkpoint (`country` namedtuple — `name`/`capital`/`continent`; `France`/`Japan`/`Senegal`; packed into `countries`)
- [x] **Review of Lambda Functions** (lambda = short anonymous function, many params but one returned value; inline at the call site or stored in a variable; `total_cost(ppsm, dim, area)` takes the area *function* as a parameter so shape isn't a branch; drawback — only suited to short/fast single-expression functions) + real checkpoint (`odd_or_even(n, even_function, odd_function)` dispatching on `n % 2`; `square`/`cube` lambdas; `odd_or_even(5, cube, square)` → **25**)
- [x] **Review of `filter()`, `map()`, and `reduce()`** (higher-order functions: iterable + processing function → iterable; imperative loop-and-append vs. declarative one-liner for each; `filter` takes a predicate, `map` a transform, `reduce` a two-parameter accumulator; `reduce` lives in `functools` in Python 3; `filter`/`map` return lazy iterators so results are wrapped in `tuple(...)`) + real checkpoints on `nums` (20 ints): `filter` evens → 14 elements; `map` ×3 → 20 elements; `reduce` sum → **328**

- [x] **Mapping a Filtered Collection** (`map(f, filter(pred, it))` reads inside-out — filter picks survivors, map transforms them; `student` namedtuple records; `q.grade <= 'B'` keeps B-or-better because string comparison is alphabetical, so the "highest" grade is the smallest string; map builds a new immutable record; 4 of 7 students → Math 201) + real checkpoints on `nums` (17 ints): `>10` doubled → **9 values** `(24, 32, 26, 38, 42, 30, 44, 40, 22)`; imperative two-loop `%3` filter + `×3` map rewritten as `map(..., filter(...))` → **(36, 27, 9, 63, 45)**

- [x] **Reducing a Filtered Collection** (`reduce(acc, filter(pred, it))`; menu as `menu_item(name, dish_type, price)` namedtuples; cheapest appetizer — imperative comprehension + running-min loop vs. one-line `reduce` with `x if x.price < y.price else y`; accumulator carries a whole record, not just a price; result **Sizzling Canadian Bacon, 9.95**) + real 12-item workspace `menu` + checkpoints: priciest entree → **Porter House Steak 131.95**; cheapest side-or-salad (`or` predicate) → **Mixed Green Salad 10.95**

- [x] **Reducing a Mapped Collection** (`reduce(acc, map(f, it))`; the `reduce` lambda's two params + return must be the same type, so a dict of `(units, price)` tuples can't be reduced directly — `map` converts each entry to a number first; iterating a dict yields its keys, so the map lambda does `costs[q][0] * costs[q][1]`; `costs` shirt/shoes/pants/socks → **537.0**, line items `(52.0, 160.0, 300.0, 25.0)`; sets up the JSON exercise later) + real checkpoint: `fruits` dict of 3-day sales tuples, map each key to its day-sum then reduce → **72** (per-fruit totals 12, 11, 14, 20, 15)

- [x] **Combining All Three Higher-Order Functions** (`reduce(acc, filter(pred, map(f, it)))` read inside-out; extended `costs` dict (+ ties, watch); map to `units × price`, filter `≤ 150`, reduce sum → **264.0**; staged breakdown shows map `(52, 160, 300, 25, 42, 145)` → filter `(52, 25, 42, 145)` → 264; the filter tests *sale values* not unit prices, so map/filter order carries meaning) + real checkpoints: sale values `> 150` summed → **460.0** (complement of 264); `nums` filter `< 10` → map `+5` → reduce product → **72648576** (filter innermost since the condition is on raw values)

- [x] **Importing Data From a CSV File** (`csv.reader` is a lazy iterator — a pointer into the file, one line per `next()`, so million-line files don't hit RAM; `house(index, square_footage, year, list_price)` namedtuple; `map` a lambda over the reader casting every string field with `int()`; `map` calls `next(reader)` itself; map/print must stay inside the `with` block; `tuple(h)` is fine for a small file, stream to text/JSON for big ones) + real checkpoint (`tree(index, width, height, volume)` namedtuple; `next(reader)` skips the header line; `mapper` casts `int`/`float`/`int`/`float`; `trees = tuple(mapper)`)

- [x] **Processing Data From a CSV File** (stack `filter`/`reduce` on the `map`-over-reader iterator instead of materializing everything; houses after 1985 via `q[2] > 1985`; priciest survivor via `reduce` carrying whole records; reader is one-shot so `houses` is materialized once; CSVs may need `.strip()` on text fields) + real checkpoint (`t = filter(lambda x: x.height > 75, mapper)` → `trees = tuple(t)`; `widest` via `reduce` on `.width`; starter strips `x[0]` before `int()`)

- [x] **Processing Data From a JSON File** (JSON = Internet/API data format; `json.load` reads the whole file into a dict, no streaming iterator unlike CSV; nested objects → nested dicts, arrays → lists; `data["cities"]` is a list of dicts; `map` each dict to a `city` namedtuple by key `x["name"]`, no casting since JSON carries types; `map` can live outside the `with`; filter/reduce stack on `cities` as before) + real checkpoint (`asia = tuple(filter(lambda q: q.continent == "Asia", cities))`; `west` = min-longitude via `reduce` on `coordinates[1]`; workspace key is `data["city"]`, not `"cities"`)

## How we work this lesson
1. You paste/describe a **sublesson's text** → I fold a concise summary + key points into the notebook.
2. You give me **Q/A** for that sublesson → I add it to the **Q & A** section (no need to ask permission — just do it).
3. You give me the **code exercise** → I add a runnable code cell under the relevant section. Your code as-is.
4. On **"done"** → final pass, update TL;DR, tick this checklist, verify the notebook runs clean, commit if asked.

## Q & A captured so far
- Modulo operator recap (remainder, divisibility/even-odd predicate, index wrapping, sign follows the right operand, works on floats) — 8/21/26
- Quick teaching reference for `map()` / `filter()` / `reduce()` (comparison table, one-line examples, how to pick, reduce expansion + seed value, laziness, `filter(None, ...)`, comprehension equivalents) — 9/9/26
- Iterator vs. iterable recap (`next()`/`StopIteration`, stateful one-shot cursor, `iter()` on a container, why `csv.reader`/`map`/`filter` are lazy) — 9/22/26
- `__next__` / iterator protocol (dunder-to-builtin mapping, hand-rolled `Countdown` iterator, how `map` chains onto `reader`) — 9/22/26
- `__init__` vs. `__iter__` vs. `__next__` (when Python calls each, container vs. iterator `__iter__`, builds/hands-out/advances) — 9/22/26
- Reader object (`csv.reader` = lazy iterator yielding a list of strings per line; not the data; tied to the `with` block; `delimiter`/`quotechar` args) — 9/22/26
- namedtuple recap (tuple with named slots, immutable, factory call returns a class, self-describing repr, use for fixed-shape records like CSV rows) — 9/22/26
- `.strip()` (both-ends whitespace removal, `lstrip`/`rstrip`, char argument, returns new string, why text CSV fields need it) — 9/23/26
- Argument shapes for `filter`/`map`/`reduce` (function first, iterable second; 1-arg predicate / 1-arg transform / 2-arg accumulator; `reduce`'s `x` is the running result; optional seed) — 9/23/26

## Open questions / to verify
- `cities.json` beside the notebook is a 7-city stand-in with the lesson's schema, stored under both `"cities"` (lesson text) and `"city"` (workspace starter code) keys so both cells run. The lesson's actual data was behind a "Select to see the JSON data" toggle and wasn't pasted.
- `trees.csv` beside the notebook is a 5-row stand-in (header + first five rows of the classic tree girth/height/volume dataset). Drop in the workspace file for matching output.
- `zillow.csv` beside the notebook is a 5-row stand-in built from the rows shown in the lesson (no header). The Codecademy workspace file is longer, so any count/total checkpoints will differ unless the full file is dropped in.
