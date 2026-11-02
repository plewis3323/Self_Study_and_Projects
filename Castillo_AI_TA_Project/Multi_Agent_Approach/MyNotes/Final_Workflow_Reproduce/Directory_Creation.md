---
title: "Directory Creation"
subtitle: "What to build before you send Multi\\_Agent\\_Outline.md to an agent"
---

# Why this matters

`Multi_Agent_Outline.md` assumes a specific folder layout. It will still
work if you hand an agent an empty directory and let it improvise one, but
every pixel coordinate the pipeline records — segment seams, figure crop
boxes — is measured against files sitting in particular places, and a
layout the agent had to invent under time pressure is more likely to drift
from the convention the outline documents elsewhere. Ten minutes creating
the right empty folders now is cheaper than a restart later.

# The layout

Create this structure inside your project root (the folder you will open
the agent in):

```
project_root/
  Input/                    Stage 0: your source handwritten/board PDFs.
                             One PDF per lecture/topic. Nothing else goes here.
  segments/                 Stage 1-2 output. Leave empty -- the agent creates
                             one subfolder per lecture as it segments.
  assembled/                Stage 3 output. Leave empty -- one approved PDF
                             per lecture lands here after the segment-review
                             loop closes.
  Final_Product_Ready/      Stage 4 output. Leave empty -- this is the
                             required name; everything else in this list may
                             be renamed, but the agent looks for this one.
    html/                   Step 4b: HTML + MathML companion, one per lecture.
    accessibility/          Step 4d: conformance reports and the
                             Accessibility Auditor's verdict, one per lecture.
  refs/                     Governing-standard sources: your institution's
                             accessibility policy PDFs, a sources.md citing
                             them. See Accessibility_Info.pdf for what belongs
                             here.
  tools/                    Copy this kit's tools/ folder here verbatim.
                             Reusable scripts the agent calls by name.
  style/                    Copy this kit's style/ folder here. Shared LaTeX
                             preamble the transcribed documents build on.
  Run_Archive/               Leave empty. Before a new run, the agent archives
                             any leftover directories from a previous job here,
                             timestamped, so a re-run never silently overwrites
                             work you meant to keep.
```

**Only `Final_Product_Ready/` is a name the pipeline requires exactly.**
Everything else is a naming convention `Multi_Agent_Outline.md` uses
throughout its own text — keeping the names matched to what the
specification says makes it easier to follow along and easier for a second
person to pick up the run later, but the agent will adapt if you rename
something and say so up front.

# What NOT to create

Do not pre-create a `For<Recipient>/` hand-off folder or try to guess its
contents — that is Stage 5 output, assembled only after every review gate in
Stages 2 and 4c/4d has closed, and its structure depends on who it is for.
Do not put anything in `segments/`, `assembled/`, or `Final_Product_Ready/`
before starting; if those folders already contain files from a previous
attempt, `Multi_Agent_Outline.md`'s own Operating Principles have the agent
archive them into `Run_Archive/` before touching them again, so a partial
prior run does not silently contaminate a new one.

# One lecture, one input file

Every source PDF in `Input/` becomes its own, separate output document —
this pipeline never merges two lectures into one deliverable, and never
splits one lecture across two. If you have four lectures to process, put
four PDFs in `Input/` and expect four documents back, each carrying its own
topic slug through `segments/<slug>/`, `assembled/<slug>.pdf`, and
`Final_Product_Ready/<slug-named-file>.tex`/`.pdf`.

# Quick checklist

- [ ] `Input/` exists and contains one PDF per lecture, nothing else
- [ ] `segments/`, `assembled/`, `Final_Product_Ready/`, `Run_Archive/` exist and are empty
- [ ] `Final_Product_Ready/html/` and `Final_Product_Ready/accessibility/` exist (or the agent will create them — either is fine)
- [ ] `tools/` and `style/` are copied in from this kit, unmodified
- [ ] `refs/` exists with your institution's accessibility policy sources, if you have them (see `Accessibility_Info.pdf`)
- [ ] You have NOT created a hand-off folder yet — that comes last

Once this is in place, move on to `Installation.pdf`, then send
`Multi_Agent_Outline.md` to your agent.
