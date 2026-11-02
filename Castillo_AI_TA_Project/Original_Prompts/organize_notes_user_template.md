# User Prompt Template: Physics Notes Organizer

Copy this template, fill in the placeholders, and attach your source images.

---

## Lecture information

- **lecture_id:** `{lecture_id}` (e.g. phys6801_2026-01-15_lagrangian)
- **course:** `{course}` (e.g. PHYS 6801 — Classical Mechanics)
- **topic:** `{topic}`
- **date:** `{date}` (YYYY-MM-DD or "unknown")
- **conversion_path_hint:** `{mathpix | direct_latex | mixed}`

## Source material

Attach all pages/scans below. List filenames you want used in `source/`:

- `{page_01.jpg}`
- `{page_02.jpg}`

## Optional context

- **Prerequisites assumed in lecture:** `{prerequisites}`
- **Notation to watch for:** `{notation}`
- **Known problem areas (blurry pages, erased board sections):** `{issues}`

## Instructions

Using the system prompt for Physics Notes Organizer, produce a complete **OrganizedNotes** package:

1. Place original scans in `OrganizedNotes/{lecture_id}/source/`.
2. Segment into blocks under `OrganizedNotes/{lecture_id}/blocks/`.
3. Write `manifest.yaml` and one `meta.yaml` per block.
4. Crop each block to `blocks/block_NNN/image.png` preserving handwriting.
5. Run the quality checklist and list any blocks needing human review.

## Output format

Return:

1. Full contents of `manifest.yaml`
2. Full contents of each `blocks/block_NNN/meta.yaml`
3. Description of each block crop (or the cropped images if your tool supports file output)
4. A short summary: block count, reading order, and blocks flagged `confidence: low`

---

## Example (minimal)

```
lecture_id: phys6801_2026-01-15_lagrangian
course: PHYS 6801 — Classical Mechanics
topic: Principle of least action
date: 2026-01-15
conversion_path_hint: mathpix

Attachments: page_01.jpg, page_02.jpg

Prerequisites: Newtonian mechanics, basic calculus of variations
Notation: S (action), L (Lagrangian), q (generalized coordinates)
Issues: bottom of page_02 is slightly out of focus
```
