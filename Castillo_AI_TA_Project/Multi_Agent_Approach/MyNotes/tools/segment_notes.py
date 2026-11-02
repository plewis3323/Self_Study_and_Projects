#!/usr/bin/env python3
"""
Stage 1 segmentation component for the multi-agent notes pipeline.

Splits a rendered page PNG into legible, logical-unit segments by finding
horizontal whitespace valleys in the ink profile. Adjacent segments are
allowed to overlap (default 55 px at 200 DPI) so nothing is lost at a cut.

Reusable: it makes no assumption about subject matter, only about the page
being dark ink on a light background (handwriting, whiteboard, chalkboard
after inversion).

Usage:
    python3 segment_notes.py PAGE_GLOB OUTDIR [--overlap N] [--min-h N] [--max-h N]
"""

import argparse
import glob
import json
import os
import sys

import numpy as np
from PIL import Image


def ink_profile(img):
    """Row-wise ink density, robust to uneven lighting (whiteboard photos)."""
    g = np.asarray(img.convert("L"), dtype=np.float32)
    # Local background = heavily blurred version of the page; ink is what is
    # meaningfully darker than its own neighbourhood.
    from PIL import ImageFilter

    bg = np.asarray(
        img.convert("L").filter(ImageFilter.GaussianBlur(radius=25)), dtype=np.float32
    )
    ink = np.clip(bg - g - 12.0, 0, None)
    mask = ink > 8.0
    return suppress_ruling(mask)


def suppress_ruling(mask, frac=0.55):
    """Drop printed ruling (graph-paper grid, margin rules) from the ink mask.

    Grid lines are dark enough to register as ink and run the full width or
    height of the page, so every row looks occupied and no whitespace valley
    is ever found. A row or column that is inked across more than `frac` of
    the page is ruling, not handwriting: the writing itself never spans that
    much. Removing them only affects where cuts are chosen -- the crops
    themselves still come from the untouched original image.
    """
    m = mask.copy()
    H, W = m.shape
    m[:, m.sum(axis=0) > frac * H] = False
    m[m.sum(axis=1) > frac * W, :] = False
    return m


def find_bands(mask, min_gap, min_ink_frac):
    """Contiguous row bands that carry ink, separated by >= min_gap blank rows."""
    w = mask.shape[1]
    row_has_ink = mask.sum(axis=1) > max(3, min_ink_frac * w)
    bands, start, gap = [], None, 0
    for y, has in enumerate(row_has_ink):
        if has:
            if start is None:
                start = y
            gap = 0
        else:
            if start is not None:
                gap += 1
                if gap >= min_gap:
                    bands.append((start, y - gap + 1))
                    start = None
                    gap = 0
    if start is not None:
        bands.append((start, len(row_has_ink)))
    return bands


def group_bands(bands, min_h, max_h, merge_gap):
    """Merge ink bands into segments of a readable size."""
    if not bands:
        return []
    groups = [list(bands[0])]
    for a, b in bands[1:]:
        cur = groups[-1]
        gap = a - cur[1]
        merged_h = b - cur[0]
        # Merge when the result is still comfortably readable, or when the
        # current group is too short to stand on its own.
        if merged_h <= max_h and (gap <= merge_gap or (cur[1] - cur[0]) < min_h):
            cur[1] = b
        else:
            groups.append([a, b])
    # A trailing sliver gets folded back into its predecessor.
    if len(groups) > 1 and (groups[-1][1] - groups[-1][0]) < min_h // 2:
        groups[-2][1] = groups[-1][1]
        groups.pop()
    return [tuple(g) for g in groups]


def snap_to_valley(mask, y, lo, hi, window):
    """Move a cut at row y to the quietest row within +/- window.

    An evenly-spaced cut lands wherever the arithmetic puts it, which is how a
    figure or a boxed equation ends up sliced in half. Nudging the cut to the
    least-inked row nearby costs nothing and keeps drawn objects whole. Ties
    resolve toward the original position so cuts stay evenly spread.
    """
    lo_w = max(lo, y - window)
    hi_w = min(hi, y + window)
    if hi_w <= lo_w:
        return y
    rows = mask[lo_w:hi_w].sum(axis=1).astype(np.int64)
    best = np.flatnonzero(rows == rows.min())
    return int(lo_w + best[np.argmin(np.abs(best - (y - lo_w)))])


def split_tall(groups, max_h, overlap, mask=None, bands=None, snap_window=110,
               hard_max_factor=2.1):
    """Any group taller than max_h is cut into overlapping slices.

    Cut placement, in order of preference:

    1. **In a gap between ink bands.** A band is a run of inked rows with no
       blank gap inside it, which is exactly what a diagram, a boxed result or
       a bracketed matrix looks like to the profiler. Cutting only in the gaps
       between bands therefore keeps drawn objects whole -- this is what stops
       a figure being sliced in half, which was the dominant defect reported by
       the Stage 2 panels.
    2. **At the quietest nearby row**, if the group holds no usable gap (a
       single band taller than max_h has to be cut somewhere).

    Cuts stay as close to evenly spaced as those constraints allow, so segments
    keep a readable, roughly uniform size.
    """
    hard_max = int(max_h * hard_max_factor)
    out = []
    for a, b in groups:
        h = b - a
        if h <= max_h:
            out.append((a, b))
            continue

        # Midpoints of the blank gaps lying strictly inside this group.
        gaps = []
        if bands:
            inner = [t for t in bands if t[0] >= a and t[1] <= b]
            for (p0, p1), (q0, q1) in zip(inner, inner[1:]):
                gaps.append((p1 + q0) // 2)

        # An oversized group with no internal gap is a single atomic block of
        # ink -- a figure, a tall bracketed matrix, a boxed derivation. Any cut
        # through it lands on content by definition, which is how figures came
        # back bisected. Keep it whole unless it is very much too tall. The
        # tolerance is deliberately generous (2.1x): on rotations p. 9 the
        # Euler-angle figure and the text above it form one continuously inked
        # 1252 px block with no blank row anywhere inside it, so any smaller
        # ceiling forces a cut straight through the figure that defines the
        # alpha/beta/gamma convention for the next four pages.
        if not gaps and h <= hard_max:
            out.append((a, b))
            continue

        n = int(np.ceil(h / max_h))
        step = int(np.ceil(h / n))

        cuts = [a]
        for i in range(1, n):
            ideal = a + i * step
            floor = cuts[-1] + max(max_h // 3, 1)
            usable = [g for g in gaps if floor <= g < b and g > cuts[-1]]
            if usable:
                cuts.append(min(usable, key=lambda g: abs(g - ideal)))
            elif mask is not None:
                cuts.append(snap_to_valley(mask, ideal, floor, b, snap_window))
            else:
                cuts.append(ideal)
        cuts.append(b)

        # A gap-aligned cut can coincide with a neighbour; drop empty slices.
        cuts = sorted(set(cuts))
        for s, nxt in zip(cuts, cuts[1:]):
            out.append((s, min(b, nxt + overlap)))
    return out


def content_columns(mask, pad, width):
    """Left/right crop bounds, so margins do not shrink the writing."""
    col = mask.sum(axis=0)
    nz = np.nonzero(col > 2)[0]
    if len(nz) == 0:
        return 0, width
    return max(0, int(nz[0]) - pad), min(width, int(nz[-1]) + pad)


def find_column_panels(mask, min_vgap, min_w):
    """Vertical panels of a wide board, split at tall blank columns.

    Whiteboard/chalkboard photos are written in columns; cutting them into
    horizontal strips would interleave unrelated derivations, so panels are
    found first and each is then segmented top-to-bottom on its own.
    """
    H, W = mask.shape
    col_has_ink = mask.sum(axis=0) > max(3, 0.012 * H)
    panels, start, gap = [], None, 0
    for x, has in enumerate(col_has_ink):
        if has:
            if start is None:
                start = x
            gap = 0
        else:
            if start is not None:
                gap += 1
                if gap >= min_vgap:
                    panels.append([start, x - gap + 1])
                    start = None
                    gap = 0
    if start is not None:
        panels.append([start, W])
    # Fold panels too narrow to be a real column into their neighbour.
    merged = []
    for p in panels:
        if merged and (p[1] - p[0]) < min_w:
            merged[-1][1] = p[1]
        elif merged and (merged[-1][1] - merged[-1][0]) < min_w:
            merged[-1][1] = p[1]
        else:
            merged.append(p)
    return [tuple(p) for p in merged] or [(0, W)]


def segment_page(path, outdir, page_no, overlap, min_h, max_h, min_gap, upscale,
                 columns=False, min_vgap=90, min_col_w=350, seg_start=1,
                 col_bounds=None, col_pad=70, hard_max_factor=2.1,
                 col_windows=None):
    img = Image.open(path)
    W, H = img.size
    mask = ink_profile(img)

    if columns:
        if col_windows:
            # Explicit per-column crop windows. Symmetric padding around a
            # shared boundary couples the right edge of one column to the left
            # edge of the next, and on a board whose lines run past the gutters
            # those two constraints can become jointly unsatisfiable. Naming
            # each window outright decouples them.
            panels = list(col_windows)
        elif col_bounds:
            edges = [0] + list(col_bounds) + [W]
            panels = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
        else:
            panels = find_column_panels(mask, min_vgap=min_vgap, min_w=min_col_w)
        idx = seg_start
        written = []
        for px0, px1 in panels:
            pad = 0 if col_windows else (col_pad if col_bounds else 15)
            sx0, sx1 = max(0, px0 - pad), min(W, px1 + pad)
            sub = img.crop((sx0, 0, sx1, H))
            smask = mask[:, sx0:sx1]
            bands = find_bands(smask, min_gap=min_gap, min_ink_frac=0.004)
            groups = group_bands(bands, min_h=min_h, max_h=max_h,
                                 merge_gap=min_gap * 2)
            groups = split_tall(groups, max_h, overlap, mask=smask, bands=bands,
                                hard_max_factor=hard_max_factor)
            if not groups:
                continue
            for a, b in groups:
                top, bot = max(0, a - overlap), min(H, b + overlap)
                crop = sub.crop((0, top, sub.width, bot))
                if upscale != 1.0:
                    crop = crop.resize(
                        (int(crop.width * upscale), int(crop.height * upscale)),
                        Image.LANCZOS,
                    )
                name = f"page{page_no:02d}_seg{idx:02d}.png"
                crop.save(os.path.join(outdir, name))
                written.append({"name": name, "page": page_no,
                                "x0": sx0, "y0": top, "x1": sx1, "y1": bot,
                                "w": crop.width, "h": crop.height})
                idx += 1
        return written

    bands = find_bands(mask, min_gap=min_gap, min_ink_frac=0.004)
    groups = group_bands(bands, min_h=min_h, max_h=max_h, merge_gap=min_gap * 2)
    groups = split_tall(groups, max_h, overlap, mask=mask, bands=bands,
                        hard_max_factor=hard_max_factor)

    if not groups:  # blank page: emit it whole rather than dropping it
        groups = [(0, H)]

    x0, x1 = content_columns(mask, pad=40, width=W)
    x0, x1 = max(0, x0 - 10), min(W, x1 + 10)

    written = []
    for i, (a, b) in enumerate(groups, start=1):
        top = max(0, a - overlap)
        bot = min(H, b + overlap)
        crop = img.crop((x0, top, x1, bot))
        if upscale != 1.0:
            crop = crop.resize(
                (int(crop.width * upscale), int(crop.height * upscale)),
                Image.LANCZOS,
            )
        name = f"page{page_no:02d}_seg{i:02d}.png"
        crop.save(os.path.join(outdir, name))
        written.append({"name": name, "page": page_no,
                        "x0": x0, "y0": top, "x1": x1, "y1": bot,
                        "w": crop.width, "h": crop.height})
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page_glob")
    ap.add_argument("outdir")
    ap.add_argument("--overlap", type=int, default=55)
    ap.add_argument("--min-h", type=int, default=230)
    ap.add_argument("--max-h", type=int, default=520)
    ap.add_argument("--min-gap", type=int, default=22)
    ap.add_argument("--upscale", type=float, default=1.0)
    ap.add_argument("--columns", action="store_true",
                    help="split wide board photos into vertical panels first")
    ap.add_argument("--min-vgap", type=int, default=90)
    ap.add_argument("--min-col-w", type=int, default=350)
    ap.add_argument("--col-windows", type=str, default="",
                    help="explicit board-panel windows, 'x0:x1,x0:x1,...'")
    ap.add_argument("--hard-max-factor", type=float, default=2.1,
                    help="how far an internally gapless block may exceed --max-h "
                         "before it is cut anyway")
    ap.add_argument("--col-pad", type=int, default=70,
                    help="half-width of the overlap at each board-panel seam")
    ap.add_argument("--col-bounds", type=str, default="",
                    help="explicit comma-separated x boundaries for board panels")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    pages = sorted(glob.glob(args.page_glob))
    if not pages:
        sys.exit(f"no pages matched {args.page_glob}")

    total = 0
    manifest = []
    for n, p in enumerate(pages, start=1):
        w = segment_page(
            p, args.outdir, n, args.overlap, args.min_h, args.max_h,
            args.min_gap, args.upscale, columns=args.columns,
            min_vgap=args.min_vgap, min_col_w=args.min_col_w,
            col_bounds=[int(v) for v in args.col_bounds.split(',') if v.strip()] or None,
            col_pad=args.col_pad, hard_max_factor=args.hard_max_factor,
            col_windows=[tuple(int(v) for v in w.split(':'))
                         for w in args.col_windows.split(',') if w.strip()] or None,
        )
        total += len(w)
        manifest.extend(w)
        print(f"{os.path.basename(p)} -> {len(w)} segments")
    with open(os.path.join(args.outdir, "segment_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(f"TOTAL {total} segments from {len(pages)} pages -> {args.outdir}")


if __name__ == "__main__":
    main()
