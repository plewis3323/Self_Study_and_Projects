# Example tagged style file

`goldsteinnotes.sty` is the style used by the HC 6001 worked example. It is
**not** a Goldstein textbook clone — it deliberately binds no physical
quantity to a letter. What you want from it on another course is the tagging
machinery:

- `\formulaalt` / `\boxeq` / `\ovaleq` — spoken `/ActualText` on boxed math
- `\tablesummary` / `\headerrows` — table summary on the Table, TH on headers
- bookmark + hyperref `/Contents` sockets
- skip `microtype` when `\GNmoderntagging` is defined (the tagged-PDF path)
- `\dbar` announced as "inexact differential" rather than "d with stroke"

Copy it, rename it, change the theorem names and the header comment. Keep
those macros. The document preamble still has to load `unicode-math` and
declare `\DocumentMetadata` — `make_accessible.py --modern` does that.

## This copy differs from the one in `Worked_Example/`

One line. `\tablesummary` walks the tag-structure stack for a Table ancestor,
and the version that built the frozen deliverable used `\tl_if_in_p:Nn` — a
predicate form expl3 does not define for `\tl_if_in:Nn`. It recovers, so
`/Summary` still lands on all three Table elements, but it costs **120
recovered TeX errors** and a non-zero `lualatex` exit status. (That exit status
is what used to kill `rebuild_example.sh` under `set -e`, after a build that
had in fact succeeded.) This template uses `\tl_if_in:NnTF`; rebuilding the
example against it gives **0 recovered errors** and a structure tree identical
to the frozen one — same 1292 elements, same 3 Tables with `/Summary`, same 7
`TH`.

`Worked_Example/Deliverable/goldsteinnotes.sty` is deliberately **left as it
was**: it is the file that produced the audited md5, and the run log discloses
this defect as known-partial item 9. Evidence of a run should not be edited
after the fact. Build new documents against the copy here.
