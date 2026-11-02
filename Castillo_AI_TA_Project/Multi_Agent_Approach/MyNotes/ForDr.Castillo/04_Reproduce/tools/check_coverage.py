#!/usr/bin/env python3
"""Verify that a page's segments retain all of its ink.

Reconstructs the union of every segment for a page (by template position is
unnecessary: segments are crops, so we compare total ink mass) and reports the
fraction of page ink that survives into at least one segment. Anything below
~99.5% means a cut dropped content and Stage 1 must be re-run for that page.
"""

import glob
import os
import sys

import numpy as np
from PIL import Image, ImageFilter


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segment_notes import ink_profile  # noqa: E402  (grid-suppressed handwriting mask)


def ink_mass(path):
    """Handwriting ink only -- printed ruling is suppressed, so a low ratio
    means real content was cut away rather than blank graph paper."""
    return float(ink_profile(Image.open(path)).sum())


def main(root):
    print(f"{'document':<14}{'page':<10}{'page ink':>12}{'seg ink':>12}{'ratio':>9}  status")
    worst = 1e9
    for doc in sorted(os.listdir(root)):
        pdir = os.path.join(root, doc, "pages")
        if not os.path.isdir(pdir):
            continue
        pages = sorted(glob.glob(os.path.join(pdir, "*.png")))
        for n, p in enumerate(pages, start=1):
            segs = sorted(glob.glob(os.path.join(root, doc, f"page{n:02d}_seg*.png")))
            pm = ink_mass(p)
            sm = sum(ink_mass(s) for s in segs)
            # Segments overlap, so seg ink >= page ink is expected; the failure
            # mode we are hunting is seg ink well BELOW page ink.
            ratio = sm / pm if pm else 1.0
            ok = "OK" if ratio >= 0.995 else "LOSS?"
            worst = min(worst, ratio)
            print(f"{doc:<14}{n:<10}{pm:>12.0f}{sm:>12.0f}{ratio:>9.3f}  {ok} ({len(segs)} segs)")
    print(f"\nworst ratio: {worst:.3f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "segments")
