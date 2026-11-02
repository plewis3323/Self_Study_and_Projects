#!/usr/bin/env python3
"""
Splice real MathML into the Formula elements whose luamml-generated /AF is an
empty shell -- the 7 `\\boxeq`/`\\ovaleq` results and the one `\\xcancel`
retraction that a box/strike hides from LuaTeX's math tagger.

Why this works and does not guess: `\\boxed`/`\\ovalbox` make the tagger treat
the whole expression as an opaque picture, so its exported MathML is a label
plus a single U+FFFD placeholder. tex4ht's make4ht route never runs that
tagger -- it renders `\\boxed` as MathML `<menclose notation='box'>` and
`\\xcancel` as `<menclose notation='updiagonalstrike downdiagonalstrike'>`,
both with the real math content inside. The HTML and PDF are built from the
same .tex source, so:
  - the 7 boxed/ovaled results are matched to the HTML by their equation
    number (the `<td class='eq-no'>(N)</td>` tex4ht writes next to every
    numbered display) -- an identity match, not a position guess;
  - the 1 unnumbered `\\xcancel` retraction is matched by its notation
    attribute, `updiagonalstrike downdiagonalstrike`, which `\\cancel` (single
    stroke) never produces and which occurs exactly once in this document.

Each empty /AF keeps its own placeholder boilerplate (the equation-label mtd,
and for boxed results the leading empty-mstyle/mrow pair luamml emits before
every equation's content) and only the trailing U+FFFD placeholder node is
replaced -- the smallest edit that fixes the content without touching
anything a downstream checker already parsed as correct.

Usage:
    python3 fix_pdf_mathml.py DOC.pdf HTML.html --out OUT.pdf
    python3 fix_pdf_mathml.py DOC.pdf HTML.html --in-place
"""

import argparse
import sys

import pikepdf
from lxml import etree

MATHML_NS = "http://www.w3.org/1998/Math/MathML"
REPLACEMENT_CHAR = "�"


def load_html_equations(html_path):
    """Return (by_number: {int: <math> element}, xcancel: <math> element | None)."""
    parser = etree.HTMLParser(recover=True)
    tree = etree.parse(html_path, parser)

    by_number = {}
    for t in tree.xpath("//table[@class='equation' and @role='presentation']"):
        eqno = t.xpath(".//td[@class='eq-no']/text()")
        maths = t.xpath(".//math")
        if not eqno or not maths:
            continue
        num_txt = eqno[0].strip().strip("()")
        if num_txt.isdigit():
            by_number[int(num_txt)] = maths[0]

    xcancel = None
    for m in tree.xpath("//math"):
        kids = [c for c in m if isinstance(c.tag, str)]
        if (len(kids) == 1 and etree.QName(kids[0]).localname == "menclose"
                and kids[0].get("notation") == "updiagonalstrike downdiagonalstrike"):
            xcancel = m
            break

    return by_number, xcancel


def clean_mathml_children(math_el):
    """Deep-copy an HTML-sourced <math> element's children, stripped of
    HTML-only cruft (class/id attributes, comments), ready to graft into a
    real MathML tree."""
    el = etree.fromstring(etree.tostring(math_el, with_tail=False))
    for e in el.iter():
        e.attrib.pop("class", None)
        e.attrib.pop("id", None)
    etree.strip_tags(el, etree.Comment)
    return list(el)  # the <math>'s children, detachable


def find_placeholder_mtext(root):
    """The lone <mtext>U+FFFD</mtext> node standing in for swallowed math."""
    for e in root.iter():
        if etree.QName(e).localname == "mtext" and (e.text or "").strip() == REPLACEMENT_CHAR:
            return e
    return None


def splice(af_bytes, replacement_math_el, label):
    root = etree.fromstring(af_bytes)
    placeholder = find_placeholder_mtext(root)
    if placeholder is None:
        raise ValueError(f"{label}: no U+FFFD placeholder found -- already fixed or shape changed")

    new_children = clean_mathml_children(replacement_math_el)
    parent = placeholder.getparent()
    idx = list(parent).index(placeholder)
    parent.remove(placeholder)
    for i, child in enumerate(new_children):
        parent.insert(idx + i, child)

    if root.get("xmlns") is None and root.tag == "math":
        root.set("xmlns", MATHML_NS)

    return etree.tostring(root, xml_declaration=False, encoding="unicode").encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("html")
    ap.add_argument("--out")
    ap.add_argument("--in-place", action="store_true")
    ap.add_argument("--boxed", type=int, nargs="*", default=[9, 10, 13, 20, 34, 37, 55],
                     help="equation numbers of the boxed/ovaled results to fix")
    args = ap.parse_args()

    if not args.out and not args.in_place:
        sys.exit("give --out OUT.pdf or --in-place")
    out_path = args.pdf if args.in_place else args.out

    by_number, xcancel_el = load_html_equations(args.html)
    missing = [n for n in args.boxed if n not in by_number]
    if missing:
        sys.exit(f"equation number(s) {missing} not found in {args.html}")
    if xcancel_el is None:
        sys.exit(f"no double-strike (xcancel) <math> found in {args.html}")

    pdf = pikepdf.open(args.pdf, allow_overwriting_input=args.in_place)

    fixed, skipped = [], []
    for obj in pdf.objects:
        try:
            if obj.get("/Type") != pikepdf.Name("/EmbeddedFile"):
                continue
        except Exception:
            continue
        data = bytes(obj.read_bytes())
        if REPLACEMENT_CHAR.encode("utf-8") not in data:
            continue
        txt = data.decode("utf-8", "replace")

        replacement_el = None
        label = None
        for n in args.boxed:
            if f"({n})" in txt.replace("  ", " "):
                replacement_el, label = by_number[n], f"eq ({n})"
                break
        if replacement_el is None and "<mtext>" in txt and len(data) < 200:
            # the unnumbered xcancel: bare <math><mtext>U+FFFD</mtext></math>
            replacement_el, label = xcancel_el, "xcancel retraction"

        if replacement_el is None:
            skipped.append((obj.objgen, len(data)))
            continue

        new_bytes = splice(data, replacement_el, label)
        obj.write(new_bytes)
        fixed.append((label, obj.objgen, len(data), len(new_bytes)))

    if len(fixed) != len(args.boxed) + 1:
        got = sorted(l for l, *_ in fixed)
        sys.exit(f"expected to fix {len(args.boxed) + 1} formulas (7 boxed/ovaled + 1 xcancel), "
                  f"fixed {len(fixed)}: {got}. Skipped (still empty, unmatched): {skipped}")

    pdf.save(out_path)
    print(f"wrote {out_path}")
    for label, objgen, old_len, new_len in sorted(fixed, key=lambda r: r[0]):
        print(f"  {label:22s} xref {objgen}: {old_len} -> {new_len} bytes")
    if skipped:
        print(f"  ({len(skipped)} other empty-looking streams left untouched: {skipped})")


if __name__ == "__main__":
    main()
