#!/usr/bin/env python3
"""
Stage 4b component: turn a plain notes .tex into a tagged, PDF/UA-targeting one.

Reusable across documents. It applies the four transforms that this toolchain
(TeX Live 2022 + latex-dev + tagpdf 0.93, testphase=phase-II) actually needs:

  1. Prepend \\DocumentMetadata so the tagging machinery is switched on at all.
  2. Load hyperxmp and set the XMP/viewer metadata veraPDF checks for
     (title, language, DisplayDocTitle, the PDF/UA part identifier).
  3. Replace \\maketitle with an explicitly tagged title block. Plain
     \\maketitle double-creates structure objects under hyperref in this
     tagpdf version and aborts the run.
  4. Wrap every \\includegraphics in an explicit Figure structure carrying
     alt text. The `alt=` key of \\includegraphics is silently ignored in
     phase-II, so the alt text has to be attached by hand via `alttext=`
     (tagpdf 0.93 spells it `alttext`, not `alt`).

Alt text is supplied per figure filename in a JSON sidecar, so the physics
and the build stay separated.

Usage:
    python3 make_accessible.py IN.tex OUT.tex ALT.json --title T --author A
"""

import argparse
import json
import re
import sys


def pdf_string_safe(s):
    """Alt text lands in a PDF string; keep it out of TeX's way."""
    return (s.replace("\\", "").replace("{", "(").replace("}", ")")
             .replace("#", "no. ").replace("%", " percent").replace("&", " and ")
             .replace("_", " ").replace("^", " ").replace("$", ""))


def add_metadata(src, title, author, lang="en-US", umath=True, modern=False):
    if modern:
        # A current LaTeX kernel tags math (with MathML), tables, lists, headings,
        # the title block and footnotes natively, and honours the alt key of
        # \includegraphics. None of the legacy workarounds below are needed.
        head = ("\\DocumentMetadata{lang=%s,pdfstandard=ua-2,pdfversion=2.0,\n"
                "  testphase={latest,math,table,sec,title,float,graphic}}\n"
                "\\def\\GNmoderntagging{}\n" % lang)
    else:
        head = "\\DocumentMetadata{lang=%s,testphase=phase-II}\n" % lang
    # Computer Modern math (CMMI/CMEX) ships no ToUnicode map, so every symbol in
    # every equation is unextractable and PDF/UA fails on it. An OpenType math
    # font under LuaTeX carries the mapping, which is what makes the math text
    # recoverable at all -- it is not a typographic preference.
    # Do not re-inject what the source already loads: a duplicated
    # \setmathfont is harmless to the build but ships a confusing preamble.
    already = "unicode-math" in src
    mathfont = ("" if (already or not umath) else
                "\\usepackage{unicode-math}\n"
                "\\setmathfont{Latin Modern Math}\n")
    if modern:
        # \DocumentMetadata writes the XMP and the PDF/UA identifier itself, so
        # hyperxmp and an explicit pdfuapart would only fight it.
        hyper = (mathfont
                 + "\\hypersetup{\n"
                   "  pdftitle={%s},\n"
                   "  pdfauthor={%s},\n"
                   "  pdflang={%s},\n"
                   "  pdfdisplaydoctitle=true,\n"
                   "}\n" % (title, author, lang))
    else:
        hyper = (
            mathfont
            + "\\usepackage{hyperxmp}\n"
            "\\hypersetup{\n"
            "  pdftitle={%s},\n"
            "  pdfauthor={%s},\n"
            "  pdflang={%s},\n"
            "  pdfdisplaydoctitle=true,\n"
            "  pdfuapart=1,\n"
            "}\n" % (title, author, lang)
        )
    # goldsteinnotes already pulls in hyperref; hyperxmp must follow it.
    if "\\usepackage{goldsteinnotes}" in src:
        src = src.replace("\\usepackage{goldsteinnotes}",
                          "\\usepackage{goldsteinnotes}\n" + hyper, 1)
    else:
        src = src.replace("\\begin{document}", hyper + "\\begin{document}", 1)
    return head + src


def tagged_title(src, title, author, date):
    block = (
        "\\begin{center}\n"
        "  \\tagstructbegin{tag=H1}\\tagmcbegin{tag=H1}%%\n"
        "  {\\LARGE\\bfseries %s\\par}%%\n"
        "  \\tagmcend\\tagstructend\n"
        "  \\vspace{8pt}\n"
        "  {\\large %s\\par}\n"
        "  \\vspace{4pt}\n"
        "  {%s\\par}\n"
        "\\end{center}\n"
        "\\vspace{6pt}\n" % (title, author, date)
    )
    if "\\maketitle" not in src:
        print("warning: no \\maketitle found; title block not inserted", file=sys.stderr)
        return src
    return src.replace("\\maketitle", block, 1)


def inline_floats(src):
    """Turn floating figures into inline centred blocks.

    A LaTeX float is typeset where the page builder puts it, but its structure
    element is appended to the tag tree at the very end of the document. In a
    7-page document that meant every figure and caption was announced after the
    final section, under a chapter on an unrelated topic, with no cue linking it
    to the text it illustrates (WCAG 1.3.2). The [H] placement from the float
    package pins each figure where it is written, so reading order matches
    visual order while the figure environment is kept intact -- which matters,
    because a Caption has to stay a child of its Figure to be conforming.
    """
    # Backslashes in a re.sub replacement are escape sequences, so pass a
    # function and return the literal text instead.
    n = src.count("\\begin{figure}")
    src = re.sub(r"\\begin\{figure\}(\[[^\]]*\])?", lambda m: "\\begin{figure}[H]", src)
    if "\\usepackage{float}" not in src:
        src = src.replace("\\begin{document}", "", 0) or src
        anchor = "\\usepackage{goldsteinnotes}"
        if anchor in src:
            src = src.replace(anchor, anchor + "\n\\usepackage{float}", 1)
        else:
            src = src.replace("\\begin{document}", "\\usepackage{float}\n\\begin{document}", 1)
    if n:
        print("pinned %d figure(s) in place for reading order" % n)
    return src


def alt_figures(src, alts):
    """Attach alt text via the native alt key of \\includegraphics."""
    pat = re.compile(r"\\includegraphics(\[[^\]]*\])?\{([^}]+)\}")
    missing, done = [], []

    def repl(m):
        opts, fn = (m.group(1) or "[]")[1:-1], m.group(2)
        alt = alts.get(fn.rsplit("/", 1)[-1])
        if not alt:
            missing.append(fn)
            return m.group(0)
        done.append(fn)
        opts = ("alt={%s}" % pdf_string_safe(alt)) + ((", " + opts) if opts else "")
        return "\\includegraphics[%s]{%s}" % (opts, fn)

    out = pat.sub(repl, src)
    if missing:
        sys.exit("FATAL: no alt text for: %s" % ", ".join(sorted(set(missing))))
    print("alt text attached to %d figures: %s" % (len(done), ", ".join(done)))
    return out


def inline_footnotes(src):
    """Turn \\footnote{...} into an inline bracketed remark.

    Footnote bodies are set by the output routine, which tagpdf 0.93 does not
    reach: the footnote text lands in the page with no marked-content at all,
    so a screen reader never sees it, and veraPDF flags it as untagged content.
    The same run also double-creates structure objects and errors out. Pulling
    the note inline keeps every word of the content and puts it in the
    structure tree where a reader can actually get to it.
    """
    out, i, n = [], 0, 0
    while True:
        j = src.find("\\footnote{", i)
        if j < 0:
            out.append(src[i:])
            break
        out.append(src[i:j])
        k = j + len("\\footnote{")
        depth = 1
        while depth:
            if src[k] == "{":
                depth += 1
            elif src[k] == "}":
                depth -= 1
            k += 1
        body = src[j + len("\\footnote{"):k - 1]
        out.append("\\ [\\emph{%s}]" % body)
        i, n = k, n + 1
    if n:
        print("inlined %d footnote(s)" % n)
    return "".join(out)


def tag_figures(src, alts):
    """Wrap each \\includegraphics in a Figure structure carrying its alt text."""
    pat = re.compile(r"\\includegraphics(\[[^\]]*\])?\{([^}]+)\}")
    missing, wrapped = [], []

    def repl(m):
        opts, fn = m.group(1) or "", m.group(2)
        key = fn.rsplit("/", 1)[-1]
        alt = alts.get(key)
        if not alt:
            missing.append(key)
            return m.group(0)
        wrapped.append(key)
        return ("\\tagstructbegin{tag=Figure,alttext={%s}}\\tagmcbegin{tag=Figure}%%\n"
                "\\includegraphics%s{%s}%%\n"
                "\\tagmcend\\tagstructend" % (pdf_string_safe(alt), opts, fn))

    out = pat.sub(repl, src)
    if missing:
        sys.exit("FATAL: no alt text for: %s\n"
                 "Every figure must have alt text before the build may proceed."
                 % ", ".join(sorted(set(missing))))
    print("tagged %d figures: %s" % (len(wrapped), ", ".join(wrapped)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("outfile")
    ap.add_argument("altfile")
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--date", default="")
    ap.add_argument("--modern", action="store_true",
                    help="target a current LaTeX kernel: native math/table/list/"
                         "heading/footnote tagging and native includegraphics alt")
    a = ap.parse_args()

    src = open(a.infile).read()
    alts = json.load(open(a.altfile))

    src = add_metadata(src, a.title, a.author, modern=a.modern)
    if a.modern:
        src = inline_floats(src)
        src = alt_figures(src, alts)
    else:
        src = tagged_title(src, a.title, a.author, a.date)
        src = inline_footnotes(src)
        src = tag_figures(src, alts)

    open(a.outfile, "w").write(src)
    print("wrote", a.outfile)


if __name__ == "__main__":
    main()
