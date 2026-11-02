#!/usr/bin/env python3
"""
Stage 1 segmentation, region-driven.

`segment_notes.py` assumes a page whose columns run top to bottom, so it takes a
set of vertical windows and cuts each one into horizontal strips. That model
breaks on a board whose lower half is written in lines running *across* the
columns: the column grid then slices those lines, and no crop shows any of them
whole. The Stage 2 panel rejected exactly that defect.

This driver takes explicit rectangles instead. A region is a piece of the page
that genuinely reads as a unit -- a column, or a band of full-width lines -- and
each is cut into overlapping strips independently, using the same whitespace
valley logic. Regions may overlap freely; a piece of content appearing whole in
one region and clipped in another is fine, because the reviewers' bar is that
every object is whole *somewhere*.

Usage:
    python3 segment_regions.py PAGE OUTDIR REGIONS.json [--upscale F]
"""

import argparse
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segment_notes import find_bands, group_bands, ink_profile, split_tall


def segment_region(img, mask, reg, overlap, min_h, max_h, min_gap):
    """Cut one rectangle into overlapping horizontal strips.

    A region marked `atomic` is emitted as a single crop instead. Some objects
    -- a figure, a boxed result, a line the writer wrapped across the page --
    only mean anything whole, and the valley finder has no way to know that: it
    reads a diagram as a tall inked block and cuts it wherever the arithmetic
    lands. Naming the rectangle and forbidding the cut is the only reliable way
    to guarantee such an object survives in one piece.
    """
    x0, y0, x1, y1 = reg["x0"], reg["y0"], reg["x1"], reg["y1"]
    if reg.get("atomic"):
        return [(x0, y0, x1, y1)]
    sub_mask = mask[y0:y1, x0:x1]
    bands = find_bands(sub_mask, min_gap=min_gap, min_ink_frac=0.004)
    groups = group_bands(bands, min_h=min_h, max_h=max_h, merge_gap=min_gap * 2)
    groups = split_tall(groups, max_h, overlap, mask=sub_mask, bands=bands)
    if not groups:
        groups = [(0, y1 - y0)]

    out = []
    for a, b in groups:
        top = max(0, a - overlap) + y0
        bot = min(y1 - y0, b + overlap) + y0
        out.append((x0, top, x1, bot))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("outdir")
    ap.add_argument("regions")
    ap.add_argument("--upscale", type=float, default=2.5)
    ap.add_argument("--overlap", type=int, default=28)
    ap.add_argument("--min-h", type=int, default=110)
    ap.add_argument("--max-h", type=int, default=230)
    ap.add_argument("--min-gap", type=int, default=12)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    img = Image.open(args.page)
    mask = ink_profile(img)
    regions = json.load(open(args.regions))

    idx, manifest = 1, []
    for reg in regions:
        rects = segment_region(img, mask, reg, args.overlap, args.min_h,
                               args.max_h, args.min_gap)
        for x0, y0, x1, y1 in rects:
            crop = img.crop((x0, y0, x1, y1))
            if args.upscale != 1.0:
                crop = crop.resize((int(crop.width * args.upscale),
                                    int(crop.height * args.upscale)),
                                   Image.LANCZOS)
            name = f"page01_seg{idx:02d}.png"
            crop.save(os.path.join(args.outdir, name))
            manifest.append({"name": name, "region": reg["name"],
                             "role": reg.get("role", ""),
                             "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                             "w": crop.width, "h": crop.height})
            idx += 1
        print(f"{reg['name']:14s} -> {len(rects)} segments")

    with open(os.path.join(args.outdir, "segment_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(f"TOTAL {len(manifest)} segments -> {args.outdir}")


if __name__ == "__main__":
    main()
