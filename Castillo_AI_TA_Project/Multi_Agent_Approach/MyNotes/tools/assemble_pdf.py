#!/usr/bin/env python3
"""
Stage 3 assembly component: paste approved segment PNGs, in reading order,
into a single PDF per document.

Segments are laid out one per page at a fixed width so every segment is
reproduced at a readable scale, and each carries its filename as a footer so
the assembled PDF can be checked back against Stage 1 output.

Usage:
    python3 assemble_pdf.py SEGDIR OUT.pdf [--title "..."]
"""

import argparse
import glob
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1700, 2200  # 8.5x11 at 200 DPI
MARGIN = 70
LABEL_H = 34


def load_font(size):
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def segment_key(path):
    """Sort by (page, segment) so reading order is preserved."""
    base = os.path.basename(path)
    try:
        page = int(base.split("page")[1].split("_")[0])
        seg = int(base.split("seg")[1].split(".")[0])
    except (IndexError, ValueError):
        return (9999, 9999, base)
    return (page, seg, base)


def render(seg_paths, out_pdf, title):
    font = load_font(22)
    tfont = load_font(40)
    pages = []

    if title:
        cover = Image.new("RGB", (PAGE_W, PAGE_H), "white")
        d = ImageDraw.Draw(cover)
        d.text((MARGIN, MARGIN), title, fill="black", font=tfont)
        d.text((MARGIN, MARGIN + 70),
               f"{len(seg_paths)} approved segments, in reading order",
               fill="black", font=font)
        pages.append(cover)

    avail_w = PAGE_W - 2 * MARGIN
    avail_h = PAGE_H - 2 * MARGIN - LABEL_H

    for p in seg_paths:
        img = Image.open(p).convert("RGB")
        scale = min(avail_w / img.width, avail_h / img.height)
        # Small segments are enlarged up to the page width; nothing is shrunk
        # below its native size unless it genuinely does not fit.
        new = img.resize((max(1, int(img.width * scale)),
                          max(1, int(img.height * scale))), Image.LANCZOS)
        page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
        x = (PAGE_W - new.width) // 2
        y = MARGIN + (avail_h - new.height) // 2
        page.paste(new, (x, y))
        d = ImageDraw.Draw(page)
        d.text((MARGIN, PAGE_H - MARGIN - LABEL_H + 6),
               os.path.basename(p), fill=(110, 110, 110), font=font)
        pages.append(page)

    if not pages:
        raise SystemExit("no segments to assemble")
    pages[0].save(out_pdf, "PDF", resolution=200.0, save_all=True,
                  append_images=pages[1:])
    return len(pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("segdir")
    ap.add_argument("out_pdf")
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    segs = sorted(glob.glob(os.path.join(args.segdir, "page*_seg*.png")),
                  key=segment_key)
    n = render(segs, args.out_pdf, args.title)
    print(f"{args.out_pdf}: {n} pages from {len(segs)} segments")


if __name__ == "__main__":
    main()
