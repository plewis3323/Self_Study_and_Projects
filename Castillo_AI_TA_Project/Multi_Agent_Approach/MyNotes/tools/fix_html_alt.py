#!/usr/bin/env python3
"""
Stage 4b companion step: repair alt text in the tex4ht/make4ht HTML output.

make4ht emits alt="PIC" for every \\includegraphics, and for any math it cannot
turn into MathML it rasterises the expression to a PNG whose alt attribute is a
fragment of leaked markup. Both are accessibility failures in the companion
document, so this pass:

  1. replaces alt="PIC" with the real alt text, keyed by image filename, using
     the same JSON sidecar the PDF build uses; and
  2. finds the rasterised-math images, marks them so a screen reader does not
     read leaked markup aloud, and reports how many there are -- that count is
     the honest measure of how much math the HTML route failed to make
     accessible, and it belongs in the run log rather than being hidden.

Usage:
    python3 fix_html_alt.py notes.html ALT.json
"""

import json
import re
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: fix_html_alt.py HTML ALT_JSON")
    path, altpath = sys.argv[1], sys.argv[2]
    html = open(path, encoding="utf-8").read()
    alts = json.load(open(altpath))

    fixed, raster = [], []

    def repl(m):
        tag = m.group(0)
        src = re.search(r'src=[\'"]([^\'"]+)', tag)
        if not src:
            return tag
        name = src.group(1).rsplit("/", 1)[-1]
        alt = alts.get(name)
        if alt:
            fixed.append(name)
            new = re.sub(r'alt=[\'"][^\'"]*[\'"]', 'alt="%s"' % alt.replace('"', "'"), tag)
            if "alt=" not in new:
                new = new.replace("<img", '<img alt="%s"' % alt.replace('"', "'"), 1)
            return new
        # Rasterised math: the alt attribute holds leaked markup. Blank it and
        # flag it rather than letting a reader announce broken tag soup.
        raster.append(name)
        new = re.sub(r'alt=[\'"][^\'"]*[\'"]', 'alt="mathematical expression, see PDF"', tag)
        return new

    # A naive <img[^>]*> stops at the first '>', which inside a rasterised-math
    # alt value lands in the middle of an embedded "<!--nolimits-->" comment. The
    # truncated tag then has no closing quote, the rewrite silently no-ops, and
    # the image ships still announcing leaked markup. Scan quote-aware instead.
    def scan_img_tags(text):
        spans, i = [], 0
        while True:
            j = text.find("<img", i)
            if j < 0:
                return spans
            k, quote = j + 4, None
            while k < len(text):
                c = text[k]
                if quote:
                    if c == quote:
                        quote = None
                elif c in "\"'":
                    quote = c
                elif c == ">":
                    break
                k += 1
            spans.append((j, k + 1))
            i = k + 1

    out, last = [], 0
    for a, b in scan_img_tags(html):
        out.append(html[last:a])
        out.append(repl(re.match(r".*", html[a:b], re.S)))
        last = b
    out.append(html[last:])
    html = "".join(out)
    open(path, "w", encoding="utf-8").write(html)

    print("figures given real alt text: %d (%s)" % (len(fixed), ", ".join(fixed)))
    print("rasterised math images found: %d" % len(raster))
    if raster:
        print("  NOT accessible as math in the HTML companion -- record in the run log")


if __name__ == "__main__":
    main()
