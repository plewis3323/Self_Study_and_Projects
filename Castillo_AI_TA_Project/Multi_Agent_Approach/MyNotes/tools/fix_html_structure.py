#!/usr/bin/env python3
"""
Repair the structural accessibility of a make4ht/tex4ht HTML companion.

The HTML route reproduces the mathematics well and the document structure
badly. Three defects come out of tex4ht every time, none of which the PDF
route has, and all of which fail the same WCAG criteria the PDF is held to:

  1. **Heading levels skip.** In `article`, \\section maps to <h3>, so the
     document runs h1 -> h3 -> h4 with no h2. Heading level is how a screen
     reader user navigates; a skipped level reads as a missing section.
  2. **Data tables have no header cells.** The header row comes out as <td>,
     so a screen reader announces a stream of cells with nothing to attach
     them to (WCAG 1.3.1).
  3. **Enumerated lists come out as definition lists.** enumitem maps
     enumerate to <dl>/<dt>/<dd>, which announces as a term/definition pair
     rather than an ordered list.

It also marks the math layout tables role="presentation": tex4ht sets display
equations in <table class="equation">, and without the role a reader is told
about dozens of tables that are not data.

    python3 fix_html_structure.py FILE.html [--data-table-class tabular]
"""

import argparse
import re
import sys
from collections import Counter


def remap_headings(h):
    """Compress heading levels so the sequence has no gaps.

    h1 is left alone; the remaining used levels are renumbered in order, so
    h1/h3/h4/h5 becomes h1/h2/h3/h4 and the nesting a screen reader reports
    matches the document's real outline.
    """
    used = sorted({int(x) for x in re.findall(r"</?h([1-6])\b", h)})
    if not used:
        return h, {}
    mapping, nxt = {}, 1
    for lv in used:
        mapping[lv] = nxt
        nxt += 1
    if mapping == {lv: lv for lv in used}:
        return h, {}
    # Rewrite via a placeholder so an h3->h2 pass cannot be re-read by a
    # later h2->h1 pass.
    def sub(m):
        slash, lv = m.group(1), int(m.group(2))
        return f"<{slash}H@{mapping[lv]}@"
    h = re.sub(r"<(/?)h([1-6])\b", sub, h)
    h = re.sub(r"<(/?)H@(\d)@", lambda m: f"<{m.group(1)}h{m.group(2)}", h)
    return h, {f"h{k}": f"h{v}" for k, v in mapping.items() if k != v}


def find_tables(h, cls):
    """Spans of every <table class="cls"> ... </table>, handling nesting."""
    out = []
    for m in re.finditer(rf"<table[^>]*class='{cls}'[^>]*>", h):
        start = m.start()
        i, depth = m.end(), 1
        while depth and i < len(h):
            nt = h.find("<table", i)
            et = h.find("</table>", i)
            if et < 0:
                break
            if 0 <= nt < et:
                depth += 1
                i = nt + 6
            else:
                depth -= 1
                i = et + 8
        out.append((start, i))
    return out


def header_cells(h, cls):
    """Promote the first non-empty data-table row to <th scope="col">.

    A \\noalign row (used to park /Summary on the Table element in the PDF)
    comes out of tex4ht as an empty <tr>. Skipping it is required: otherwise
    that empty row is treated as the header and the real header stays <td>.
    """
    n_tables = n_cells = 0
    for start, end in reversed(find_tables(h, cls)):
        block = h[start:end]
        rows = list(re.finditer(r"<tr\b.*?</tr>", block, re.S))
        if not rows:
            continue
        target = None
        for row_m in rows:
            text = re.sub(r"<[^>]+>", " ", row_m.group(0))
            text = re.sub(r"&nbsp;", " ", text, flags=re.I)
            if text.strip():
                target = row_m
                break
        if target is None:
            continue
        row = target.group(0)
        if "<th" in row and "<td" not in row:
            continue
        new = re.sub(r"<td\b", "<th scope='col'", row)
        new = new.replace("</td>", "</th>")
        cells = new.count("<th")
        if not cells:
            continue
        block = block[:target.start()] + new + block[target.end():]
        h = h[:start] + block + h[end:]
        n_tables += 1
        n_cells += cells
    return h, n_tables, n_cells


def table_captions(h, cls):
    """Give each data table a <caption> taken from its figure caption.

    Acrobat reports a missing table summary as *skipped*, which is a silent
    omission rather than a pass, so the summary is attached to the table
    itself instead of only to the surrounding figure.
    """
    n = 0
    for start, end in reversed(find_tables(h, cls)):
        block = h[start:end]
        if "<caption" in block:
            continue
        before = h[:start]
        m = None
        for m in re.finditer(r"<figcaption[^>]*>(.*?)</figcaption>", before, re.S):
            pass
        if not m:
            continue
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        open_tag = re.match(r"<table[^>]*>", block).group(0)
        block = open_tag + f"<caption>{text}</caption>" + block[len(open_tag):]
        h = h[:start] + block + h[end:]
        n += 1
    return h, n


def presentation_tables(h, data_cls):
    """Mark non-data layout tables as presentational."""
    def sub(m):
        tag = m.group(0)
        if f"class='{data_cls}'" in tag or "role=" in tag:
            return tag
        return tag[:-1] + " role='presentation'>"
    return re.sub(r"<table[^>]*>", sub, h)


def enumerate_lists(h):
    """Turn tex4ht's <dl class="enumerate-*"> back into a real <ol>."""
    n = 0
    for m in reversed(list(re.finditer(
            r"<dl class='(enumerate[^']*)'>(.*?)</dl>", h, re.S))):
        body = m.group(2)
        items = re.findall(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", body, re.S)
        if not items:
            continue
        # The <dt> holds the marker (1., 2., ...) which <ol> supplies itself.
        lis = "".join(f"<li>{b.strip()}</li>" for _, b in items)
        h = h[:m.start()] + f"<ol class='enumerate'>{lis}</ol>" + h[m.end():]
        n += 1
    return h, n


def audit(h):
    imgs = re.findall(r"<img\b[^>]*>", h)
    return {
        "mathml": len(re.findall(r"<math\b", h)),
        "headings": dict(sorted(Counter(re.findall(r"<h(\d)\b", h)).items())),
        "img_without_alt": sum(1 for i in imgs if "alt=" not in i),
        "img_alt_PIC": sum(1 for i in imgs if 'alt="PIC"' in i or "alt='PIC'" in i),
        "th": len(re.findall(r"<th\b", h)),
        "table_caption": len(re.findall(r"<caption\b", h)),
        "ol_ul": len(re.findall(r"<[uo]l\b", h)),
        "lang": bool(re.search(r"<html[^>]*\blang=", h)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--data-table-class", default="tabular")
    a = ap.parse_args()

    h = open(a.html, encoding="utf-8").read()
    cls = a.data_table_class

    h, hmap = remap_headings(h)
    h, nt, nc = header_cells(h, cls)
    h, ncap = table_captions(h, cls)
    h, nl = enumerate_lists(h)
    h = presentation_tables(h, cls)

    open(a.html, "w", encoding="utf-8").write(h)

    print(f"heading levels remapped : {hmap or 'no change needed'}")
    print(f"data tables given TH    : {nt} ({nc} header cells)")
    print(f"table captions added    : {ncap}")
    print(f"enumerate -> ol         : {nl}")
    print("layout tables marked role=presentation")
    print("\npost-repair audit:")
    for k, v in audit(h).items():
        print(f"  {k:20s} {v}")


if __name__ == "__main__":
    main()
