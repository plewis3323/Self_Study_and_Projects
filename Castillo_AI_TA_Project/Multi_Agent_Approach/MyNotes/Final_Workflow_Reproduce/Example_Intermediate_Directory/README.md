# Example intermediate evidence

This is the Stage 1–3 output for the same run `Example_Deliverable_Directory/`
shows the Stage 4 output of — the segmented pages, the Stage 2 review loop,
and the assembled pre-LaTeX PDF that fed Stage 4a's transcription. Stage 5's
own hand-off requirements (`Multi_Agent_Outline.md` Success Criterion 21)
call this "the intermediate evidence," and this is what it actually looks
like for a real run, not a description of it.

| File / folder | What it is |
|---|---|
| `segments/` | Stage 1's output for this lecture: `page01_seg01.png` … one PNG per logical unit, `segment_manifest.json` (the authoritative inventory — see Stage 1's "never infer the segment list" rule), `alt_text.json` and `figure_crops.json` as drafted at crop time (before Stage 4b re-reads them through the sidecar), `segment_run.json` (the render engine/dpi record), and `review_log.md` — the Stage 2 loop: three independent reviewers, round by round, until all three returned APPROVE. |
| `assembled/scattering_hamiltonian_approved.pdf` | Stage 3's output: the approved segments pasted in reading order into one PDF. This is what Stage 4a's reference-textbook choice and Stage 4b's transcription are performed against. |
| `notes_src.tex` | The Stage 4b transcription **before** `make_accessible.py` tags it — plain LaTeX, no `\DocumentMetadata`, no `alt=` keys yet. Compare this against `Example_Deliverable_Directory/hc6001_2024-10-22_scattering_hamiltonian.tex` to see exactly what the accessibility build step adds. |

Frozen alongside `Example_Deliverable_Directory/` — do not edit these to match
a later tool change, and do not write your own lecture's intermediates here.
