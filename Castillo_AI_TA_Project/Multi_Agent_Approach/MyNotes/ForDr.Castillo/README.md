# HC 6001 — accessible edition, 22 October 2024 lecture

Start with **`00_PROCESS_REPORT.md`**. It opens with what is still wrong,
answers the WCAG 2.1 AA / 7 Core Skills / MDAS checklist row by row, and says
which of the two formats to publish.

- `01_Deliverable/` — the tagged PDF, its LaTeX source, and the HTML companion
- `02_Accessibility_Evidence/` — conformance reports, measured test results,
  the full auditor report, and `verify.sh` to re-run every check yourself
- `03_Source_Input/` — the untouched source
- `04_Reproduce/` — run log, manifest, specification, and all tools
- `05_Intermediate/` — approved segments and the segmentation manifest

To verify: `cd 02_Accessibility_Evidence && ./verify.sh /path/to/verapdf`
