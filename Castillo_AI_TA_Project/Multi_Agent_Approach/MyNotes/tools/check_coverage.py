#!/usr/bin/env python3
"""Verify that a page's segments cover all of its ink.

**This test used to compare ink *mass*: the sum of ink over all segments
against the ink on the page.** Segments overlap by design, so segment mass
runs 20-40% above page mass and the ratio never approached the failure
threshold -- the check could not fail, and a pass from it was worth nothing.
It is replaced here by a coverage test on *rows*, which can fail:

  1. Take the page's ink-row profile with the same mask the segmenter uses.
  2. Take each segment's [y0, y1) span from segment_manifest.json.
  3. Report the ink rows no segment span contains.

An uncovered ink row is content that was cut away, and no amount of overlap
hides it. Rows covered twice are fine and are reported separately, because
that is what overlap is for.

Coverage is judged inside the page's *content band* (segment_seams'
`content_bounds`), which is the region the segmenter itself works in. Ink rows
outside that band are counted and named rather than silently dropped: on a
poppler render of US Letter the final row carries a handful of edge pixels on
every page, and calling that lost content would make the test cry wolf on a
correct run. `--strict` folds those rows back into the verdict.

    python3 check_coverage.py SEGDIR [--pages DIR] [--manifest FILE]
                              [--max-uncovered 0]

SEGDIR is a slug directory holding segment_manifest.json (pages default to
SEGDIR/pages, the layout Stage 1 writes). Exits non-zero when a page has more
uncovered ink rows than --max-uncovered, so it can gate the pipeline.
"""

import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segment_seams import content_bounds, ink_profile  # noqa: E402


def page_file(pagedir, n):
    for pat in (f"page-{n}.png", f"page{n:02d}.png", f"page-{n:02d}.png"):
        p = os.path.join(pagedir, pat)
        if os.path.exists(p):
            return p
    hits = sorted(glob.glob(os.path.join(pagedir, "*.png")))
    return hits[n - 1] if len(hits) >= n else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("segdir", help="slug directory holding segment_manifest.json")
    ap.add_argument("--pages", default=None, help="page rasters (default SEGDIR/pages)")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--threshold", type=int, default=None,
                    help="ink pixels per row to count as a content row "
                         "(default: the manifest's own ink_row_threshold)")
    ap.add_argument("--max-uncovered", type=int, default=0,
                    help="uncovered ink rows tolerated per page (default 0)")
    ap.add_argument("--strict", action="store_true",
                    help="also fail on ink rows outside the content band "
                         "(render edge artifacts land there)")
    args = ap.parse_args()

    man_path = args.manifest or os.path.join(args.segdir, "segment_manifest.json")
    if not os.path.exists(man_path):
        raise SystemExit(f"no manifest at {man_path} -- Stage 1 writes it; "
                         f"never infer the segment list from filenames")
    with open(man_path) as fh:
        manifest = json.load(fh)

    pagedir = args.pages or os.path.join(args.segdir, "pages")
    if not os.path.isdir(pagedir):
        raise SystemExit(f"no page rasters at {pagedir} (pass --pages)")

    thresh = args.threshold
    if thresh is None:
        thresh = int(manifest[0].get("ink_row_threshold", 2)) if manifest else 2

    by_page = {}
    for seg in manifest:
        by_page.setdefault(int(seg["page"]), []).append(seg)

    print(f"{'page':<6}{'ink rows':>10}{'covered':>10}{'uncovered':>11}"
          f"{'2+ covered':>12}  status")
    worst = 0
    failed = []
    outside_total = 0
    for pg in sorted(by_page):
        pf = page_file(pagedir, pg)
        if pf is None:
            print(f"{pg:<6}{'-':>10}{'-':>10}{'-':>11}{'-':>12}  NO PAGE RASTER")
            failed.append(pg)
            continue

        prof, height, _ = ink_profile(pf)
        ink_rows = prof >= thresh

        top, bot = content_bounds(prof)
        band = np.zeros(height, dtype=bool)
        band[top:bot] = True
        if not args.strict:
            outside = int((ink_rows & ~band).sum())
            outside_total += outside
            ink_rows = ink_rows & band

        cover = np.zeros(height, dtype=np.int16)
        for seg in by_page[pg]:
            y0 = max(0, int(seg["y0"]))
            y1 = min(height, int(seg["y1"]))
            cover[y0:y1] += 1

        n_ink = int(ink_rows.sum())
        uncovered = int((ink_rows & (cover == 0)).sum())
        covered = n_ink - uncovered
        overlapped = int((ink_rows & (cover >= 2)).sum())
        ok = uncovered <= args.max_uncovered
        worst = max(worst, uncovered)
        if not ok:
            failed.append(pg)

        status = "OK" if ok else "LOSS"
        print(f"{pg:<6}{n_ink:>10}{covered:>10}{uncovered:>11}{overlapped:>12}"
              f"  {status} ({len(by_page[pg])} segs, content band y{top}-{bot})")

        if uncovered:
            rows = np.flatnonzero(ink_rows & (cover == 0))
            runs, start = [], rows[0]
            for a, b in zip(rows, rows[1:]):
                if b != a + 1:
                    runs.append((int(start), int(a)))
                    start = b
            runs.append((int(start), int(rows[-1])))
            for a, b in runs[:6]:
                print(f"        uncovered rows y{a}-{b} "
                      f"({b - a + 1} rows of ink outside every segment)")

    print(f"\nworst uncovered ink rows on any page: {worst}")
    if outside_total:
        print(f"{outside_total} ink row(s) lay outside the content band and "
              f"were excluded (render edge artifacts). Re-run with --strict "
              f"to hold the segmentation to them as well.")
    if failed:
        print(f"FAIL: pages {sorted(set(failed))} lose ink. Re-cut those pages "
              f"(Stage 1) before the review loop sees them.")
        sys.exit(1)
    print("PASS: every ink row on every page falls inside at least one segment.")


if __name__ == "__main__":
    main()
