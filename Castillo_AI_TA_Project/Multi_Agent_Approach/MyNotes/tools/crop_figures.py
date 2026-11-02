#!/usr/bin/env python3
"""
Stage 1 -- cut the deliverable's figures out of the page rasters.

Operating Principle 8: every figure in the final document is a crop of the
source drawing, never a redrawing. This makes that crop reproducible. The
boxes live in figure_crops.json, keyed by *final figure filename*:

    "scat_fig2_repulsive.png": {
      "source_page": 1,
      "box_as_rendered": [x0, y0, x1, y1],   # pixels in the page render
      "render_dpi": 300                       # which render those pixels are in
    }

`box_300dpi` is the same rectangle expressed at 300 dpi so boxes stay
comparable across renders; `box_as_rendered` is what is actually cut. A figure
needing more resolution than the segmentation render carries a higher
`render_dpi` and is cut from a page rendered at that dpi (in the reference run,
one figure at 600).

    python3 crop_figures.py CROPS.json PAGEDIR OUTDIR [--check] [--prefix page]

PAGEDIR holds page-N.png from render_pages.py. For any figure whose render_dpi
differs from PAGEDIR's, pass --extra-pages DPI=DIR so the crop is taken from a
page rendered at that dpi rather than upscaled.

--check re-cuts every figure and compares against the PNGs already in OUTDIR
pixel by pixel, reporting identical / differing rather than overwriting. That
is the reproducibility test: same source PDF plus same boxes must give back
the same figures.
"""

import argparse
import json
import os
import sys

import numpy as np
from PIL import Image


def page_path(pagedir, prefix, n):
    return os.path.join(pagedir, f"{prefix}-{n}.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("crops")
    ap.add_argument("pagedir")
    ap.add_argument("outdir")
    ap.add_argument("--prefix", default="page")
    ap.add_argument("--extra-pages", action="append", default=[],
                    metavar="DPI=DIR",
                    help="pages rendered at another dpi, e.g. 600=pages_600")
    ap.add_argument("--check", action="store_true",
                    help="compare against existing PNGs instead of writing")
    args = ap.parse_args()

    with open(args.crops) as fh:
        crops = json.load(fh)

    # which page directory serves which dpi
    base_dpi = None
    rj = os.path.join(args.pagedir, "render.json")
    if os.path.exists(rj):
        base_dpi = json.load(open(rj)).get("dpi")
    dirs = {}
    if base_dpi:
        dirs[int(base_dpi)] = args.pagedir
    for spec in args.extra_pages:
        dpi, _, d = spec.partition("=")
        dirs[int(dpi)] = d

    os.makedirs(args.outdir, exist_ok=True)
    ok = same = diff = missing = 0

    for name, spec in crops.items():
        pg = spec["source_page"]
        dpi = int(spec.get("render_dpi", base_dpi or 300))
        box = spec.get("box_as_rendered") or spec["box_300dpi"]

        pdir = dirs.get(dpi, args.pagedir)
        src = page_path(pdir, args.prefix, pg)
        if not os.path.exists(src):
            print(f"[MISS] {name}: needs page {pg} at {dpi} dpi ({src}). "
                  f"Render it, or pass --extra-pages {dpi}=DIR.")
            missing += 1
            continue

        im = Image.open(src).convert("RGB")
        x0, y0, x1, y1 = box
        if x1 > im.width or y1 > im.height:
            print(f"[FAIL] {name}: box {box} falls outside the "
                  f"{im.width}x{im.height} render of page {pg} at {dpi} dpi. "
                  f"Wrong dpi, or a box measured against a different render.")
            missing += 1
            continue
        cut = im.crop((x0, y0, x1, y1))

        want = spec.get("size")
        if want and list(cut.size) != list(want):
            print(f"[WARN] {name}: cut is {cut.size}, manifest says {tuple(want)}")

        dst = os.path.join(args.outdir, name)
        if args.check:
            if not os.path.exists(dst):
                print(f"[MISS] {name}: nothing at {dst} to compare against")
                missing += 1
                continue
            have = np.asarray(Image.open(dst).convert("RGB"))
            got = np.asarray(cut)
            if have.shape == got.shape and np.array_equal(have, got):
                print(f"[SAME] {name}  {cut.size}")
                same += 1
            else:
                where = ("shape" if have.shape != got.shape
                         else f"{int((have != got).any(axis=2).sum())} px")
                print(f"[DIFF] {name}  differs: {where}")
                diff += 1
        else:
            cut.save(dst)
            print(f"[CUT ] {name}  {cut.size}  <- page {pg} @{dpi} dpi {box}")
            ok += 1

    if args.check:
        print(f"\nidentical {same}, differing {diff}, missing {missing}")
        sys.exit(1 if (diff or missing) else 0)
    print(f"\n{ok} figure(s) -> {args.outdir}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
