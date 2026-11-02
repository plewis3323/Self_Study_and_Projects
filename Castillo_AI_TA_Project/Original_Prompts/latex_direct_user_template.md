# User Prompt Template: Direct LaTeX from OrganizedNotes (Step 3b)

Copy this template and paste the OrganizedNotes contents below (or attach files).

---

## Target

- **Output file:** `{lecture_id}.tex`
- **OrganizedNotes path:** `OrganizedNotes/{lecture_id}/` or `Main_Project/examples/sample_lecture/`

## Instructions

Using the Step 3b system prompt, convert the OrganizedNotes package below into a single compilable LaTeX file.

Include block traceability comments (`% block_NNN`) and `% REVIEW:` flags where metadata indicates low/medium confidence.

---

## manifest.yaml

```yaml
{paste manifest.yaml here}
```

---

## Block metadata (in reading_order)

### block_001/meta.yaml

```yaml
{paste meta.yaml}
```

### block_002/meta.yaml

```yaml
{paste meta.yaml}
```

(repeat for each block)

---

## Optional: block images

Attach or reference:

- `blocks/block_001/image.png`
- `blocks/block_002/image.png`

If images are attached, treat them as authoritative for notation.

---

## Expected response

1. Full contents of `{lecture_id}.tex`
2. Brief validation report:
   - blocks covered vs `reading_order`
   - any `% REVIEW:` or `% UNCLEAR:` flags added
   - packages required to compile

---

## Example invocation (sample lecture)

```
Output file: sample_lecture_lagrangian.tex
OrganizedNotes path: Main_Project/examples/sample_lecture/

Use manifest.yaml and all three block meta.yaml files in reading_order.
No block images available — use metadata only; mark block_003 with REVIEW per its review_notes.
```
