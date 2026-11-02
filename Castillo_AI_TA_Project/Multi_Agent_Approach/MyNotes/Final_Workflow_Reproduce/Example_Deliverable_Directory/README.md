# Example deliverable

This is a real, complete output of this pipeline run on
`../Example_Input_Directory/Lecture-scattering-Hamiltonian_241022-forward.pdf`
— the same shape `Final_Product_Ready/` will hold for each of your own
lectures once a run finishes. This exact copy passed six rounds of
independent physics review, the Accessibility Auditor's own review loop,
and — as of its current md5 — a live PAC 2026 run showing **0 Failed
checkpoints**.

| File / folder | What it is |
|---|---|
| `hc6001_2024-10-22_scattering_hamiltonian.pdf` | The finished, tagged, PDF/UA-1-conformant deliverable. |
| `hc6001_2024-10-22_scattering_hamiltonian.tex` | Its LaTeX source — read this to see what "transcribed to the pipeline's conventions" actually looks like: real sectioning, `\formulaalt` spoken math on boxed/struck results, `\erratum`-flagged source errors, figure alt text passed through `alt_text.json`. |
| `goldsteinnotes.sty` | The shared preamble this document (and yours) builds on. |
| `figures/` | High-fidelity crops of the original drawing, embedded via `\includegraphics`, never redrawn. |
| `html/` | The required HTML + MathML companion, held to the same accessibility bar as the PDF. |
| `alt_text.json` | The alt-text sidecar every figure's `\includegraphics` draws from. |
| `errata.json` | Source transcription errors, flagged rather than silently fixed, per this pipeline's own policy. |
| `MANIFEST.json` | The run's own machine-readable record: inputs, the input→slug→output mapping, toolchain versions, and a `closed_from_*`/`known_gaps` trail for every review round and every post-close addendum — including `accessibility.pac_2026_review`, the synthesized verdict `auditor_report.md`'s addenda point back to. |
| `accessibility/` | Every accessibility artifact Step 4d produces: veraPDF UA-1/UA-2 reports, the four mandatory structural test results (`structure_tests.json`), measured contrast, the reading-order and screen-reader walks, and the Accessibility Auditor's full written verdict (`auditor_report.md`) — including its own addenda documenting defects found and fixed *after* the initial round closed. Also holds the real, operator-run **PAC 2026** evidence those addenda narrate: `pac_2026_detailed_report_2026-08-20.md` (the transcribed checkpoint-level detail PAC's GUI does not export) and the two PAC summary-PDF exports (`pac_2026_summary_report_2026-08-20.pdf` / `_run2.pdf`, before and after the UA-1 switch and tagging-defaults fix). Read `auditor_report.md` in full; it is the most concrete example in this kit of what "measure, don't assert" looks like applied to a real document. |

This folder is frozen as a reference — do not edit it to match a later tool
change, and do not write your own lecture into it. If you rebuild it
yourself with `Reproduce.pdf`'s instructions, compare structure counts
against what is here rather than expecting a byte-identical file.
