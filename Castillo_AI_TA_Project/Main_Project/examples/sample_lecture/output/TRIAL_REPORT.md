# Step 3b Trial Run — sample_lecture_lagrangian

Trial date: 2026-06-24

## Input

- `manifest.yaml` — 3 blocks, 2 sections
- `blocks/block_001/meta.yaml` through `block_003/meta.yaml`
- No block images (metadata-only run)

## Prompts used

- System: [latex_direct_system_prompt.md](../../../Original_Prompts_Precontext_files/latex_direct_system_prompt.md)
- User template: [latex_direct_user_template.md](../../../Original_Prompts_Precontext_files/latex_direct_user_template.md)

## Output

- LaTeX: [sample_lecture_lagrangian.tex](sample_lecture_lagrangian.tex)
- PDF: [sample_lecture_lagrangian.pdf](sample_lecture_lagrangian.pdf) (if compile succeeded)

## Validation report

| Check | Result |
|-------|--------|
| Blocks in `reading_order` covered | 3/3 (block_001, block_002, block_003) |
| Sections match manifest | action_principle → §1; euler_lagrange → §2 |
| `% block_NNN` traceability | Present on all blocks |
| `% REVIEW:` flags | block_003 (confidence: medium, smudged notation) |
| Invented content | None beyond standard EL form implied by metadata |
| Packages | amsmath, amssymb, amsthm, graphicx, geometry |

## Notes

- Without block images, equations were taken from `equations_detected` and standard graduate mechanics notation.
- When real `image.png` files exist, re-run with images attached so notation matches the professor's handwriting.
