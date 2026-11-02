# Sources for Accessible Notes Conversion Project

PDF snapshots saved 2026-08-08, of pages retrieved and read during the 2026-08-07
accessibility-requirements research session (see `AI-answers/accessible-notes-conversion-pipeline_260807.txt`
for the full session log, and `../Multi_Agent_Outline_Accessibility.md` for the pipeline revision these
informed). Pages were captured by rendering the live URL to PDF (headless Chromium), so formatting/layout
may differ slightly from a manual "Save as PDF" from a browser, but text content is complete.

| File | Source | URL |
|---|---|---|
| `01_OU-news-DOJ-extension-260505.pdf` | Ohio University News | https://www.ohio.edu/news/2026/05/doj-extends-digital-accessibility-deadlines-ohio-university-continues-progress |
| `02_OU-news-faculty-deadline-260200.pdf` | Ohio University News | https://www.ohio.edu/news/2026/02/new-federal-digital-accessibility-deadline-what-ohio-faculty-need-know |
| `03_OU-OIT-digital-accessibility-guidelines.pdf` | OHIO Office of Information Technology | https://www.ohio.edu/oit/accessibility/guidelines |
| `04_OU-OIT-accessible-documents.pdf` | OHIO Office of Information Technology | https://www.ohio.edu/oit/accessibility/guidelines/accessible-documents |
| `05_OU-OIT-faculty-course-checklist.pdf` | OHIO Office of Information Technology | https://www.ohio.edu/oit/accessibility/guidelines/course-checklist |
| `06_FederalRegister-Title-II-deadline-extension.pdf` | Federal Register (via govinfo.gov, the official GPO mirror — federalregister.gov itself blocks automated retrieval) | https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web (PDF fetched from: https://www.govinfo.gov/content/pkg/FR-2026-04-20/pdf/2026-07663.pdf) |

## What each document establishes

1. **01 — DOJ extension announcement (OHIO News, May 2026):** confirms Ohio University's compliance deadline moved to **April 26, 2027** under the DOJ's one-year extension, and that a cross-campus working group (Accessibility Services, OIT, University Communications and Marketing) is coordinating the response.
2. **02 — Faculty guidance (OHIO News, Feb 2026, pre-extension):** states the (then-current) April 24, 2026 deadline and lists what's in scope for faculty: Canvas course content, **documents and PDFs**, website materials, video/audio, images/tables. Names the "7 core skills" faculty are asked to apply.
3. **03 — OIT Digital Accessibility Guidelines (overview):** landing page for OHIO's guideline set; confirms WCAG 2.1 Level AA as the adopted standard; links out to the topic-specific pages below.
4. **04 — OIT Accessible Documents guideline:** the PDF-specific guidance. Recommends avoiding PDFs where possible; for PDFs that must remain, describes structural-tag remediation (headings, reading order, alt text, table markup) and names **PAC 2026** (Windows-only, via Company Portal) as the recommended checking tool; states OCR is required first for scanned-original PDFs; states OHIO has **no in-house remediation service** and points to external vendors for complex cases. Contains no math/LaTeX/STEM-specific content.
5. **05 — Faculty Checklist for Accessible Content:** the 13-item practical checklist (alt text, contrast, links, accessibility-checker use, PDFs, captions, transcripts, tables, syllabus statement, etc.) faculty are asked to apply per course. Contains no math/LaTeX/STEM-specific content.
6. **06 — Federal Register, DOJ Title II compliance-date extension (April 20, 2026):** the actual regulatory text extending compliance dates for the ADA Title II web/mobile accessibility rule — the primary legal source underlying all of the above; specifies the population-based deadline tiers (large entities April 26, 2027; smaller/special-district entities April 26, 2028) and the WCAG 2.1 AA technical standard.

## Not included here

General web-search results that were only skimmed as search snippets (not opened/read in full) are not captured as PDFs — only pages whose content was actually read and used are included above. If you want additional pages captured (e.g. OHIO's Accessibility Services office page, or a specific Canvas/Ally page), let me know and I'll add them the same way.
