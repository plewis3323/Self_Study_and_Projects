---
title: "Accessibility Info"
subtitle: "What standard this pipeline targets, and why a clean checker is not the evidence"
---

# The standard, briefly

This pipeline targets **WCAG 2.1 Level AA**, the technical standard the
DOJ's ADA Title II rule sets for web and mobile content at public
universities (compliance date for larger institutions: April 26, 2027 —
the requirements did not change with that date's extension, only the
deadline did). **WCAG2ICT** is the clause that brings a standalone PDF
into scope at all; without it, WCAG reads as a web-only standard. On the
PDF side, that translates to **PDF/UA** conformance plus a set of
Minimum Digital Accessibility Standards (MDAS) many universities check as
a floor:

1. Accessibility permission flag is set (nothing blocks assistive tech).
2. The PDF has a title.
3. The PDF has full text — not image-only.
4. Document language is specified.
5. Every figure has alternative text.

If you are adapting this pipeline for a different institution, check its
own accessibility policy for the specifics — the WCAG/PDF-UA/MDAS
combination above is common but not universal, and `refs/` is where this
kit keeps the source documents for whichever institution it targets, so an
agent never has to guess or take a claim on faith.

# UA-1 or UA-2 — this is a real choice, and it matters which

PDF/UA has two versions. **UA-2** (2024, requires PDF 2.0) has richer math
tagging — equations can carry their MathML as an Associated File (`/AF`)
rather than needing an explicit spoken alt text on every formula. **UA-1**
(2014, PDF 1.4-1.7) predates that mechanism and does not recognize `/AF` as
alternative text at all — a document declaring UA-2 with `/AF`-only math
will show every equation without a hand-authored description as *failing*
a UA-1 check.

This matters because **the checker your reviewer will actually run may only
implement UA-1.** PAC 2026 — the tool many institutions point their
reviewers at — checks against UA-1 specifically (confirmed by reading its
own report header, not assumed). A document that is honestly, defensibly
UA-2-conformant can still come back from an institutional review flagged
for missing alternative text on nearly every equation, because the reviewer's
tool was never checking what the document declared. **Match your declared
standard to what will actually check it, not to which standard has the
nicer feature set.** This kit's own `Multi_Agent_Outline.md` defaults to
UA-1 for exactly this reason — see its Toolchain Prerequisites section for
the full account of switching, including the kernel mechanism that makes it
possible without hand-authoring hundreds of formula descriptions from
scratch.

# A conformance pass is a floor, not evidence

This is the single most important thing on this page, and it is not a
platitude — it is a repeated, specific finding from building this pipeline:

- A checker returned a **clean pass three separate times** on a document
  that had 16 headings mis-tagged as ordinary paragraphs (no navigable
  outline at all), 24 content operators sitting completely outside the tag
  tree, and one table cell marked as decorative artifact — silently
  deleting the word "Quantum" from a Classical-vs-Quantum comparison and
  inverting its meaning for anyone using a screen reader.
- This pipeline's *own* verification script once reported "0 empty
  equations" while 8 equations were exporting nothing but a blank
  placeholder character, because the check compared *counts* instead of
  matching each formula to its own result by identity.
- A table's `/Summary` — required for an accessible data table — was
  written to the wrong place in the PDF's internal structure for months.
  Every internal test that checked "does a summary exist" said yes. The
  actual PDF specification does not recognize that location as valid at
  all, so a real accessibility reviewer's tool saw no summary whatsoever.
  Nothing about this was visible without checking the *specific location*
  a summary attribute is supposed to live in, not just whether the string
  was present somewhere in the file.

The pattern in all three: **the checker was answering a different, easier
question than the one that mattered**, and every one of them returned a
confident, clean, wrong answer. Treat any single tool's pass — including
this kit's own scripts — as a floor to build from, never as proof of
anything on its own.

# What actually catches these things

`Multi_Agent_Outline.md`'s Step 4d runs veraPDF (the conformance floor)
plus four mandatory numeric tests that are what actually caught every
defect above:

1. **Structure-element inventory** — every heading in the source must
   produce exactly the matching number of tagged headings, correctly
   nested. (Catches: headings silently tagged as plain paragraphs.)
2. **Content reachability** — every piece of visible text must be either
   marked as decoration or reachable from the tag tree. Zero unreachable
   operators, no exceptions. (Catches: content technically present but
   invisible to assistive technology.)
3. **Artifact audit** — list everything marked as decorative and confirm
   none of it is actually meaningful content. (Catches: a data cell wrongly
   marked as page furniture.)
4. **Figure reading position** — no figure or table may cluster at the very
   end of the document's reading order regardless of where it sits
   visually on the page. (Catches: floats silently relocating their own
   tag-tree position away from the text that explains them.)

None of these are exotic. All four are scriptable (`tools/check_structure.py`
runs them together) and none of them take more than a few seconds to run —
the expensive part was ever discovering they were necessary, not running
them once known.

# When a checker itself is behind the standard

Institutional checkers update on their own schedule, not the standard's.
If a checker's own dialog admits it does not fully support the PDF version
your document uses, that is not something to argue with abstractly — verify
directly whether the specific findings it reports still hold against your
own file (structure-tree inspection, independent text extraction) before
either dismissing them or chasing them blind. Sometimes the finding is real
and the checker's version limitation is irrelevant to it; sometimes it
isn't. The only way to know is to check, per finding, not to assume either
way from the disclaimer alone.

# Reviewer roles this pipeline uses, and why one of them cannot be overruled

`Multi_Agent_Outline.md` assigns an independent **Accessibility Auditor**
whose APPROVE/REVISE verdict a physics content reviewer cannot waive, and
the reverse: the auditor cannot waive a physics reviewer's verdict either.
This split exists because visual quality and structural accessibility are
genuinely independent properties of the same file — a document can be
typographically excellent and completely unusable with a screen reader, or
vice versa — and a single reviewer optimizing for one will not reliably
catch failures in the other. Expect the Accessibility Auditor to be the
last reviewer still saying REVISE in most rounds. That is by design, not a
bottleneck to route around.
