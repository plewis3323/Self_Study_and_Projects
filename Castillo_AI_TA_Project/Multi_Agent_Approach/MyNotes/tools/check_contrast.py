#!/usr/bin/env python3
"""
Measure WCAG contrast where this pipeline can actually lose it.

Two jobs, because the deliverable has two kinds of visual content:

  images   ink-versus-background on each figure crop. These stay raster, so
           they inherit whatever contrast pencil-on-paper had. WCAG 1.4.11
           wants non-text indicators at >= 3:1.
  pdf      the colour every text run is actually painted in, against the page.
           WCAG 1.4.3 wants text at >= 4.5:1. Link colours are the usual
           offender -- hyperref's defaults do not reliably clear it.

    python3 check_contrast.py --images FIG_DIR [--fix OUTDIR]
    python3 check_contrast.py --pdf DOC.pdf

--fix raises any crop under 3:1 by a levels stretch on the ink channel and
writes the result to OUTDIR, reporting before/after. It never redraws: the
strokes are the source strokes, only their tone changes.
"""

import argparse
import glob
import json
import os
import sys
from collections import Counter

import numpy as np
from PIL import Image


def rel_luminance(rgb):
    """WCAG relative luminance from 0-255 sRGB."""
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def ratio(l1, l2):
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def ink_layers(a):
    """Split a crop into its pen layers plus the printed ruling.

    The discriminator between cyan ruling and blue pen is GREEN, not blue:
    the ruling is cyan (G-R ~ +95), the pen is violet (G-R ~ +12). Filtering
    on "not much bluer than red" drops the blue pen and the red strike-through
    with it.
    """
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(axis=2), a.min(axis=2)
    dark = mx < 235
    ruling = dark & ((B - R) >= 45) & ((G - R) >= 60)
    red = dark & ((R - G) > 60) & ((R - B) > 60)
    # Guard blue on GREEN as well, mirroring the segmentation mask. Testing
    # only "bluer than its own minimum" admits anti-aliased ruling that just
    # missed the ruling test, which then appears as a blue-pen layer of a
    # couple of hundred pixels in figures that contain no blue pen at all.
    blue = dark & ~ruling & ~red & ((B - R) >= 45) & ((G - R) < 30)
    black = dark & ~ruling & ~red & ~blue
    return {"black pen": black, "blue pen": blue,
            "red pen": red, "printed ruling": ruling}


def measure_image(path, min_px=500):
    """Each ink layer's tone against the paper it sits on.

    A single ink figure hides the layer that fails. Black pen on white is
    ~21:1 and masks a blue stroke at half that, so one number reads as a clean
    pass whatever else is on the page. Measure the layers separately and let
    the worst one decide.
    """
    a = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64)
    lum = rel_luminance(a)
    bg = float(np.quantile(lum.ravel(), 0.90))
    layers, worst = {}, None
    for name, mask in ink_layers(a).items():
        n = int(mask.sum())
        if n < min_px:
            continue
        # A crumb of anti-aliased ruling that missed the ruling test can
        # register as a "blue pen" layer of a figure that has none. Ignore a
        # named pen layer that is under 2% of all dark pixels when another
        # pen layer is already present -- 1.6% of the pixels is not a stroke.
        dark_n = int((lum < (bg * 0.75)).sum()) if bg else 0
        if (name != "printed ruling" and dark_n and n < 0.02 * dark_n
                and n < 5000):
            continue
        # Report the layer's REPRESENTATIVE colour, not its darkest tail. A
        # stroke is anti-aliased, so its 2nd-percentile pixel is far darker
        # than the ink a reader actually sees and flatters the ratio; the
        # median pixel is the stroke's real tone.
        px = a[mask.astype(bool)]
        rep = tuple(int(v) for v in np.median(px, axis=0))
        l = float(rel_luminance(np.array(rep, dtype=np.float64)))
        r = round(ratio(bg, l), 2)
        layers[name] = {"px": n, "representative_rgb": rep,
                        "luminance": round(l, 4), "ratio": r,
                        "darkest_2pct_ratio": round(
                            ratio(bg, float(np.quantile(lum[mask], 0.02))), 2)}
        # The verdict is about the drawing. Printed graph-paper ruling is not
        # content a reader needs, so it is measured and reported but excluded
        # from the worst-layer verdict -- stated here rather than left implicit.
        if name != "printed ruling" and (worst is None or r < worst[1]):
            worst = (name, r)

    # Two ink layers separable only by hue vanish into one another in
    # greyscale or in print. That is WCAG 1.4.1: if colour is the only thing
    # telling two objects apart, the text has to say which is which.
    pens = {k: v for k, v in layers.items() if k != "printed ruling"}
    names = sorted(pens)
    pairs = {f"{names[i]} vs {names[j]}":
             round(ratio(pens[names[i]]["luminance"], pens[names[j]]["luminance"]), 2)
             for i in range(len(names)) for j in range(i + 1, len(names))}

    return {"bg_luminance": round(bg, 4),
            "layers": layers,
            "ratio": worst[1] if worst else round(ratio(bg, 0.0), 2),
            "worst_layer": worst[0] if worst else None,
            "greyscale_separation": pairs}


def boost(path, out, target=3.0):
    """Deepen the ink until it clears `target`, preserving the strokes."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im, dtype=np.float64)
    before = measure_image(path)["ratio"]
    if before >= target:
        return before, before, False
    lum = rel_luminance(a)
    bg = float(np.quantile(lum.ravel(), 0.90))
    # Solve for the ink luminance that reaches the target against this paper.
    want = (bg + 0.05) / target - 0.05
    g = a.copy()
    dark = lum < (bg * 0.75)
    for c in range(3):
        ch = g[..., c]
        ch[dark] = np.clip(ch[dark] * 0.35, 0, 255)   # deepen strokes only
        g[..., c] = ch
    Image.fromarray(g.astype(np.uint8)).save(out)
    after = measure_image(out)["ratio"]
    return before, after, True


def measure_pdf(path):
    """Every distinct fill colour used by text, with its contrast to the page."""
    try:
        import fitz
    except ImportError:
        sys.exit("--pdf needs PyMuPDF")
    doc = fitz.open(path)
    page_lum = rel_luminance((255, 255, 255))
    seen = Counter()
    worst = None
    for pno, page in enumerate(doc, 1):
        d = page.get_text("dict")
        for blk in d.get("blocks", []):
            for ln in blk.get("lines", []):
                for sp in ln.get("spans", []):
                    col = sp.get("color", 0)
                    rgb = ((col >> 16) & 255, (col >> 8) & 255, col & 255)
                    r = ratio(page_lum, rel_luminance(rgb))
                    key = (rgb, round(r, 2))
                    seen[key] += len(sp.get("text", ""))
                    if worst is None or r < worst[1]:
                        worst = (rgb, r, pno, sp.get("text", "")[:40])
    return {"colors": [{"rgb": k[0], "ratio": k[1], "chars": v}
                       for k, v in seen.most_common()],
            "lowest": {"rgb": worst[0], "ratio": round(worst[1], 2),
                       "page": worst[2], "sample": worst[3]} if worst else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images")
    ap.add_argument("--pdf")
    ap.add_argument("--fix")
    ap.add_argument("--target", type=float, default=3.0)
    ap.add_argument("--json")
    a = ap.parse_args()
    out = {}

    if a.images:
        rows = []
        if a.fix:
            os.makedirs(a.fix, exist_ok=True)
        print(f"=== figure crops (WCAG 1.4.11 non-text: >= {a.target}:1) ===")
        for f in sorted(glob.glob(os.path.join(a.images, "*.png"))):
            m = measure_image(f)
            row = {"file": os.path.basename(f), **m}
            if a.fix:
                dst = os.path.join(a.fix, os.path.basename(f))
                b, af, changed = boost(f, dst, a.target)
                if not changed:
                    Image.open(f).save(dst)
                row["ratio_before"], row["ratio_after"] = b, af
                row["adjusted"] = changed
            rows.append(row)
            flag = "OK " if m["ratio"] >= a.target else "LOW"
            extra = (f"  -> {row['ratio_after']}:1 (adjusted)"
                     if a.fix and row.get("adjusted") else "")
            layers = " ".join(f"{k.split()[0]}{v['representative_rgb']}={v['ratio']}"
                              for k, v in m["layers"].items())
            print(f"  [{flag}] {row['file']:32s} worst {m['ratio']:6.2f}:1"
                  f"  ({m['worst_layer']}){extra}")
            print(f"        layers: {layers}")
            for pair, r in m["greyscale_separation"].items():
                if r < 3.0:
                    print(f"        COLOUR-ONLY RISK: {pair} separate by only "
                          f"{r}:1 in greyscale -- name the difference in words")
        out["images"] = rows
        out["verdict_excludes"] = (
            "printed ruling -- the pre-printed graph-paper grid. It is not "
            "content a reader needs in order to understand the drawing, so it "
            "is excluded from the WCAG 1.4.11 verdict, but it is measured and "
            "its ratio is reported so the exclusion is visible rather than "
            "silent.")
        low = [r for r in rows if (r.get("ratio_after") or r["ratio"]) < a.target]
        print(f"  lowest: {min(r.get('ratio_after') or r['ratio'] for r in rows):.2f}:1"
              f"   below target: {len(low)}")

    if a.pdf:
        m = measure_pdf(a.pdf)
        out["pdf"] = m
        print(f"\n=== built PDF text colours (WCAG 1.4.3 text: >= 4.5:1) ===")
        for c in m["colors"]:
            flag = "OK " if c["ratio"] >= 4.5 else "LOW"
            print(f"  [{flag}] rgb{c['rgb']}  {c['ratio']:6.2f}:1   {c['chars']} chars")
        if m["lowest"]:
            print(f"  lowest: {m['lowest']['ratio']}:1 on page {m['lowest']['page']}"
                  f"  ({m['lowest']['sample']!r})")

    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
        print(f"\nwrote {a.json}")


if __name__ == "__main__":
    main()
