#!/usr/bin/env python3
"""
Stage 1 segmentation by measured seams, with protected no-cut bands.

Differs from segment_notes.py in two ways that matter on ruled paper:

1. **Ink is identified by colour, not by darkness.** Graph-paper ruling is blue
   (B >> R) while handwriting is neutral dark. A luminance-only profile counts
   every grid line as content, finds no valleys at all, and then cuts wherever
   the target height falls -- straight through whatever is there.

2. **Diagram bands can be declared un-cuttable.** A seam through a figure is
   the expensive defect in this pipeline: the drawing is also the deliverable's
   figure, so a bad cut is not just a readability problem.

    python3 segment_seams.py PAGE_GLOB OUTDIR [--target 820] [--overlap 140]
                             [--protect "1:1500-2010,3:2080-2340"]

--protect takes `page:y0-y1` bands, comma separated, in page-pixel coordinates.
"""

import argparse
import glob
import json
import os
import re
import sys

import numpy as np
from PIL import Image


def ink_mask(a):
    """Every pen stroke, excluding the printed ruling.

    The obvious rule -- dark, and not much bluer than red -- separates black
    ink from cyan ruling and then silently discards two things that matter:
    blue pen (B-R is large for it too) and red strike-through (not dark in R
    at all). On these pages that rule sees 0.2% of an 11k-pixel retraction
    mark, so the mark is invisible to coverage and seam arithmetic alike.

    The discriminator that separates the layers is GREEN: the ruling is cyan
    (G-R ~ +95) while blue pen is violet (G-R ~ +12). Keep anything that is
    either dark OR strongly coloured, and reject only the cyan ruling -- the
    second half matters because saturated red is not dark in any channel.
    """
    mx, mn = a.max(axis=2), a.min(axis=2)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    ruling = ((B - R) >= 45) & ((G - R) >= 60)
    # Saturated red has max(RGB)=255, so a darkness cap alone classifies the
    # whole retraction mark as paper. Anything strongly coloured counts as ink
    # whether or not it is dark.
    return ((mx < 235) | ((mx - mn) >= 60)) & ~ruling


def ink_profile(path):
    """Row-wise count of pen pixels of any colour."""
    a = np.asarray(Image.open(path).convert("RGB"), dtype=np.int16)
    ink = ink_mask(a)
    return ink.sum(axis=1), a.shape[0], a.shape[1]


def parse_protect(spec):
    bands = {}
    for part in filter(None, (p.strip() for p in spec.split(","))):
        m = re.match(r"^(\d+)\s*:\s*(\d+)\s*-\s*(\d+)$", part)
        if not m:
            sys.exit(f"bad --protect entry: {part!r} (want page:y0-y1)")
        bands.setdefault(int(m.group(1)), []).append((int(m.group(2)), int(m.group(3))))
    return bands


INK_ROW_THRESHOLD = 2


def content_bounds(prof, thresh=12):
    """First and last row carrying real content.

    The threshold is not 1: a scan carries a few stray pixels at the sheet
    edge, and treating those as content stretches the page's content band to
    the paper edge, which then drags every seam on the page with it.
    """
    nz = np.flatnonzero(prof > thresh)
    return (int(nz[0]), int(nz[-1]) + 1) if len(nz) else (0, len(prof))


def pick_seams(prof, top, bot, target, protect, min_h):
    """Greedy: from `top`, jump ~target rows, then slide to the quietest row.

    The search window is +/-45% of target, and any row inside a protected band
    is disqualified outright rather than merely penalised.
    """
    seams = []
    y = top
    n = len(prof)
    # A wide smoothing kernel finds the *band* that is quiet, not a lucky row.
    k = 21
    sm = np.convolve(prof.astype(float), np.ones(k) / k, mode="same")
    while bot - y > target * 1.55:
        lo = max(y + min_h, int(y + target * 0.55))
        hi = min(bot - min_h, int(y + target * 1.45))
        if hi <= lo:
            break
        cand = [r for r in range(lo, hi)
                if not any(a <= r <= b for a, b in protect)]
        if not cand:
            # Entirely inside a protected band: jump past the band and retry.
            end = max(b for a, b in protect if a <= hi and b >= lo)
            if end <= y:
                break
            y = min(end + 1, bot)
            continue
        seam = min(cand, key=lambda r: (sm[r], abs(r - (y + target))))
        seams.append(seam)
        y = seam
    return seams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page_glob")
    ap.add_argument("outdir")
    ap.add_argument("--target", type=int, default=820)
    ap.add_argument("--overlap", type=int, default=140)
    ap.add_argument("--min-h", type=int, default=300)
    ap.add_argument("--protect", default="")
    ap.add_argument("--pad-top", type=int, default=40)
    a = ap.parse_args()

    protect = parse_protect(a.protect)
    os.makedirs(a.outdir, exist_ok=True)
    manifest = []

    for pno, path in enumerate(sorted(glob.glob(a.page_glob)), 1):
        prof, H, W = ink_profile(path)
        top, bot = content_bounds(prof)
        top = max(0, top - a.pad_top)
        bot = min(H, bot + a.pad_top)
        bands = protect.get(pno, [])
        seams = pick_seams(prof, top, bot, a.target, bands, a.min_h)

        cuts = [top] + seams + [bot]
        img = Image.open(path)
        for i in range(len(cuts) - 1):
            y0 = cuts[i] if i == 0 else max(top, cuts[i] - a.overlap)
            y1 = cuts[i + 1]
            name = f"page{pno:02d}_seg{i+1:02d}.png"
            img.crop((0, y0, W, y1)).save(os.path.join(a.outdir, name))
            manifest.append({"name": name, "page": pno,
                             "x0": 0, "y0": int(y0), "x1": W, "y1": int(y1),
                             "w": W, "h": int(y1 - y0),
                             # One threshold, emitted with the counts, so the
                             # manifest is reproducible from the tool that
                             # wrote it rather than from a remembered setting.
                             "ink_row_threshold": INK_ROW_THRESHOLD,
                             "ink_rows": int((prof[y0:y1] > INK_ROW_THRESHOLD).sum()),
                             "ink_px": int(prof[y0:y1].sum())})
        print(f"{os.path.basename(path)}: content y{top}-{bot}, "
              f"seams {seams} -> {len(cuts)-1} segments")

    with open(os.path.join(a.outdir, "segment_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    with open(os.path.join(a.outdir, "segment_run.json"), "w") as fh:
        json.dump({"invocation": {"target": a.target, "overlap": a.overlap,
                                  "min_h": a.min_h, "protect": a.protect,
                                  "pad_top": a.pad_top},
                   "ink_row_threshold": INK_ROW_THRESHOLD,
                   "segments": len(manifest)}, fh, indent=1)
    print(f"TOTAL {len(manifest)} segments -> {a.outdir}")


if __name__ == "__main__":
    main()
