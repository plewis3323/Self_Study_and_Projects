#!/usr/bin/env python3
"""
Stage 1, step 0 -- render each source PDF page to a PNG.

Everything downstream of this works on page rasters, not on the PDF:
segment_seams.py and segment_notes.py take a glob of page PNGs, and
crop_figures.py cuts the deliverable's figures out of these same rasters.
Render once, at a stated dpi, and record it -- a crop box measured against a
300 dpi page means nothing if the page was later re-rendered at 200.

    python3 render_pages.py INPUT.pdf OUTDIR [--dpi 300] [--prefix page]

Writes OUTDIR/page-1.png ... and OUTDIR/render.json (the renderer, the dpi and
the page sizes, so a later stage can convert a box between resolutions instead
of guessing).

**The renderer is part of the measurement.** Crop boxes and seam rows are pixel
coordinates in a particular raster, and two rasterisers do not agree pixel for
pixel: poppler's `pdftoppm` and PyMuPDF differ in antialiasing, and on US
Letter at 300 dpi they do not even agree on the page height (3301 vs 3300
rows). Re-render a page with the other engine and every recorded box shifts
underneath you. This script therefore prefers `pdftoppm`, which is what
produced the reference run's rasters -- it reproduces them bit for bit -- and
falls back to PyMuPDF only when poppler is absent, recording which was used.
If render.json says `pymupdf` and the manifest was measured under `pdftoppm`,
re-measure; do not reuse the boxes.

The reference run rendered at 300 dpi for segmentation and re-rendered page 2
at 600 dpi for one small figure crop; both dpi values are recorded in
figure_crops.json as `render_dpi`. 300 dpi is the floor for handwriting: at
150 dpi a pencil stroke is two pixels wide and the ink mask cannot separate it
from the paper.
"""

import argparse
import glob
import json
import os
import shutil
import subprocess


def parse_pages(spec):
    """'2' or '1,3-4' -> a sorted list of 1-based page numbers."""
    if not spec:
        return None
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return sorted(out)


def render_poppler(pdf, outdir, dpi, prefix, pages):
    """pdftoppm: the renderer the reference run used."""
    cmd = ["pdftoppm", "-png", "-r", str(dpi)]
    if pages:
        # pdftoppm takes a contiguous range; call it once per run of pages
        # rather than pretending a comma list works.
        runs = []
        for p in pages:
            if runs and p == runs[-1][1] + 1:
                runs[-1][1] = p
            else:
                runs.append([p, p])
    else:
        runs = [None]
    for run in runs:
        c = list(cmd)
        if run:
            c += ["-f", str(run[0]), "-l", str(run[1])]
        c += [pdf, os.path.join(outdir, prefix)]
        subprocess.run(c, check=True)
    # pdftoppm zero-pads when the document has 10+ pages; normalise to page-N
    for f in glob.glob(os.path.join(outdir, f"{prefix}-*.png")):
        base = os.path.basename(f)
        num = base[len(prefix) + 1:-4]
        want = os.path.join(outdir, f"{prefix}-{int(num)}.png")
        if f != want:
            os.replace(f, want)


def render_pymupdf(pdf, outdir, dpi, prefix, pages):
    """Fallback. Does NOT match pdftoppm pixel for pixel -- see the header."""
    import fitz  # imported here so poppler-only machines need no PyMuPDF

    doc = fitz.open(pdf)
    mat = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    for i, page in enumerate(doc, start=1):
        if pages and i not in pages:
            continue
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB, alpha=False)
        pix.save(os.path.join(outdir, f"{prefix}-{i}.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--dpi", type=int, default=300,
                    help="render resolution (default 300; do not go below it)")
    ap.add_argument("--prefix", default="page",
                    help="output basename, numbered from 1 (default 'page')")
    ap.add_argument("--pages", default="",
                    help="1-based page list, e.g. '2' or '1,3-4' (default all)")
    ap.add_argument("--engine", choices=["auto", "pdftoppm", "pymupdf"],
                    default="auto",
                    help="auto prefers pdftoppm (the reference renderer)")
    args = ap.parse_args()

    if args.dpi < 300:
        print(f"WARNING: {args.dpi} dpi is below the 300 dpi floor for "
              f"handwriting; the ink mask will struggle.")

    os.makedirs(args.outdir, exist_ok=True)
    pages = parse_pages(args.pages)

    engine = args.engine
    if engine == "auto":
        engine = "pdftoppm" if shutil.which("pdftoppm") else "pymupdf"
    if engine == "pdftoppm" and not shutil.which("pdftoppm"):
        raise SystemExit("pdftoppm not found (install poppler-utils)")

    if engine == "pdftoppm":
        render_poppler(args.pdf, args.outdir, args.dpi, args.prefix, pages)
    else:
        print("NOTE: rendering with PyMuPDF. Boxes measured under pdftoppm do "
              "not transfer; re-measure seams and crops against these rasters.")
        render_pymupdf(args.pdf, args.outdir, args.dpi, args.prefix, pages)

    written = []
    from PIL import Image
    for f in sorted(glob.glob(os.path.join(args.outdir, f"{args.prefix}-*.png")),
                    key=lambda p: int(os.path.basename(p)[len(args.prefix) + 1:-4])):
        n = int(os.path.basename(f)[len(args.prefix) + 1:-4])
        if pages and n not in pages:
            continue
        w, h = Image.open(f).size
        written.append({"page": n, "file": os.path.basename(f), "px": [w, h]})
        print(f"{f}  {w}x{h} px  @{args.dpi} dpi  ({engine})")

    if not written:
        raise SystemExit("no pages rendered -- check --pages")

    meta = {"source": os.path.abspath(args.pdf), "dpi": args.dpi,
            "engine": engine, "pages": written}
    with open(os.path.join(args.outdir, "render.json"), "w") as fh:
        json.dump(meta, fh, indent=1)

    print(f"\n{len(written)} page(s) -> {args.outdir}  "
          f"(render.json records engine={engine}, dpi={args.dpi})")


if __name__ == "__main__":
    main()
