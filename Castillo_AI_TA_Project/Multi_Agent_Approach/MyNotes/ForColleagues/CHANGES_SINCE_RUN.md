# What changed after the reference run

`Worked_Example/` is the 16 August 2026 run, frozen. Its PDF, logs, manifest
and evidence are exactly as they were audited — md5
`85b05d31081368d8b811063456c7f769` — and nothing here edits them. The tooling
around them has moved on, and this page says how, so a number in the run log
that no longer matches a tool's behaviour reads as history rather than as a
contradiction.

## Two tools were missing from the kit

Stage 1 began with a page raster, and nothing in `tools/` produced one; the
figure crops were likewise cut by hand from boxes recorded in
`figure_crops.json`. An agent handed this kit had to invent both steps, and an
invented render step is not a small thing — it silently changes the coordinate
system every seam row and crop box in the manifest is written in.

- **`render_pages.py`** — PDF → page rasters at a recorded dpi. It prefers
  `pdftoppm`, which is what the reference run used and what reproduces its
  rasters bit for bit, falls back to PyMuPDF, and records which engine ran in
  `render.json`. The two do not agree: on US Letter at 300 dpi poppler emits
  3301 rows and PyMuPDF 3300, and their antialiasing differs throughout.
- **`crop_figures.py`** — cuts the figures from `figure_crops.json`, honouring
  a per-figure `render_dpi`. `--check` re-cuts and compares pixel by pixel
  instead of writing.

Both are verified against the frozen run: `./verify.sh --reproduce` re-derives
the four page rasters, all fifteen segments and all five figures from
`Worked_Example/Input/` and finds them identical.

## `check_coverage.py` could not fail; now it can

It compared total ink *mass* across segments against the page. Segments
overlap by 20–40 % by design, so the ratio never approached its threshold — the
check was incapable of reporting loss, and the run log said so (known-partial
item 8). It now tests **row coverage**: every ink row inside the page's content
band must fall inside at least one segment span from the manifest. It exits
non-zero and names the uncovered row ranges. Confirmed both ways — it passes
the frozen segmentation, and it reports 614 lost rows when a segment is removed
from the manifest.

## `style/goldsteinnotes.sty` lost 120 recovered TeX errors

`\tablesummary` walked the tag-structure stack with `\tl_if_in_p:Nn`, a
predicate form expl3 does not define for `\tl_if_in:Nn`. It recovers, so
`/Summary` still landed on all three Table elements, but every build carried
120 recovered errors and exited non-zero — known-partial item 9 in the run log.
The template here uses `\tl_if_in:NnTF`. Rebuilt against it, the example gives
**0 recovered errors** and a structure tree identical to the frozen one: 1292
elements, 3 Tables with `/Summary`, 7 `TH`, 16 headings.

`Worked_Example/Deliverable/goldsteinnotes.sty` keeps the old line on purpose —
it is the file that produced the audited md5. Build new documents against
`style/`.

## `rebuild_example.sh` no longer dies on a successful build

LuaLaTeX exits non-zero on recovered errors and still writes a complete PDF.
Under `set -e` that killed the script after the third pass, before it printed
an md5 or ran a single structural test: a rebuild that had in fact succeeded
looked like a silent failure. It now accounts for the exit status, reports the
recovered-error count as a number, and carries on to the checks.

## `verify.sh --reproduce` is new

The deliverable's md5 proves the file you were sent is the file that was
audited. It says nothing about whether the pipeline that produced it still
works on your machine. `--reproduce` answers that second question in about a
minute, without LaTeX.

## A real PAC 2026 run (2026-08-20) found two tagging defects; a new post-build fix closes them

Someone actually ran PAC 2026 against `Worked_Example/Deliverable/`'s frozen
PDF and got its detailed checkpoint view, not just the summary page — the
first time this pipeline had that. Two findings were real and traced to a
root cause (not patched blind) before anything was fixed:

- **All 7 `TH` cells failed "no associated data cells."** `/Scope` reaches
  them only through `/C /TH-col` + `/ClassMap` — conformant PDF, and the
  mechanism this pipeline deliberately chose, but apparently not one PAC
  resolves (PAC's own dialog admits incomplete PDF 2.0 support).
- **57/58 "Part" and 8/8 "Note" warnings** — every ordinary paragraph and
  every figure/table float wrapper, traced by walking the PDF's own
  `/RoleMap` with pikepdf, turned out to be **latex-lab's own built-in
  default role table** for the `pdf2`/UA-2 namespace, not anything this
  document's `.sty` or transcription chose.

`tools/fix_pdf_tagging_defaults.py` (new, same family as
`fix_pdf_mathml.py`) fixes both post-build: adds a literal `/A` to each `TH`
duplicating the `ClassMap`-resolved `/Scope`, and remaps `RoleMap
/text-unit → /P` and `/float → /Div`. Additive/redirective only — no
content, MCID, or reading-order change; verified clean against veraPDF
UA-1/UA-2 and the full Step 4d numeric-test suite before shipping.

**`Worked_Example/Deliverable/` was deliberately left unpatched** — it is
frozen evidence of the 16 August audit and stays exactly as audited, md5
`85b05d31...`. The fix went into the *live* pipeline's own deliverable
(`Final_Product_Ready/`, superseding md5 `f6e5c207...` with `0c4d468a...`),
and `tools/fix_pdf_tagging_defaults.py` is now shipped in this kit's own
`tools/`, so a new build from this kit can run it too. Full narrative:
`Multi_Agent_Outline.md`'s home-repo `PIPELINE_LOG.md`, 2026-08-20 "same
day" entry.

## The kit's default `\DocumentMetadata` now declares UA-1, not UA-2

Same day, second change: `Multi_Agent_Outline.md`'s own required-setup
example (Step 4b, and the toolchain-probe preamble) switched from
`pdfstandard=ua-2,pdfversion=2.0` to `pdfstandard=ua-1,pdfversion=1.7`.
Reason: **PAC 2026 — the checker Ohio University reviewers actually run —
checks against UA-1**, and UA-1's clause 7.7 does not recognize UA-2's
`/AF`-only math tagging as alternative text at all. A document built to
this kit's *old* default would show every equation without a hand-authored
spoken rendition as missing alt text under PAC, no matter how clean its
other tagging was.

`ua-1` is a real, kernel-supported target (`g__pdfmeta_standard_pdf/UA-1_prop`
in `latex-lab`'s own `pdfmanagement.ltx`), not a workaround: on UA-1
detection the kernel auto-writes `/Alt` on every Formula element (the raw
LaTeX source, e.g. `s = \frac{\ell}{\sqrt{2mE}}` — real, non-empty, and
conformant, but lower quality than a hand-authored `\formulaalt` spoken
rendition; disclose that gap rather than claim it fully solved). Verified
on the scattering-Hamiltonian document before shipping: veraPDF UA-1
flipped FAIL→PASS, all 198 Formulas went from 9/198 to 198/198 carrying
alt text or `ActualText`, 0 recovered errors across 3 lualatex passes, no
other Step 4d test regressed.

**If you build a new document from this kit**, use the updated
`\DocumentMetadata` in `Multi_Agent_Outline.md`/`style/`'s conventions
(`pdfstandard=ua-1, pdfversion=1.7`) unless you have a specific reason to
target UA-2 instead — and if you do, expect PAC to keep flagging bare
Formulas the way this kit's own worked example did before this change.
`Worked_Example/Deliverable/` (frozen, `85b05d31...`) still declares UA-2
and was not touched. Full narrative: `PIPELINE_LOG.md`'s second 2026-08-20
"same day" entry.
