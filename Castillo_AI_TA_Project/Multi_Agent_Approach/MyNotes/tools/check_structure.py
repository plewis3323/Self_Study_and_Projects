#!/usr/bin/env python3
"""
Step 4d structural acceptance tests for a tagged PDF, in one pass.

Implements the four mandatory numeric tests from the pipeline outline, plus the
list/table structure counts, the MathML non-emptiness check, the alt-text audit
against the sidecar, and the metadata check. Every test prints a number and a
PASS/FAIL line; the exit status is non-zero if any acceptance criterion fails.

    python3 check_structure.py DOC.pdf [--alt alt_text.json]
                               [--sections N] [--json out.json]

--sections N is the count of sectioning commands in the .tex (\\section +
\\subsection + ...). Test 1 compares the H-element count against it.

Subject-independent: nothing here knows about physics.

Why the tests exist at all: in the reference run veraPDF returned a clean pass
in three consecutive audits while 16 headings were tagged as paragraphs and 24
content operators sat outside the tag tree. A checker pass is a floor.
"""

import argparse
import json
import re
import sys
import zlib
from collections import Counter

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("check_structure.py needs PyMuPDF:  pip install pymupdf")


# --------------------------------------------------------------------------
# raw object access
# --------------------------------------------------------------------------

def all_streams(path):
    """Concatenate every stream in the file, inflating what inflates.

    Used only for coarse counting (MathML blocks, tag-name frequencies); the
    structural tests below walk real objects instead.
    """
    raw = open(path, "rb").read()
    out = bytearray()
    for m in re.finditer(rb"stream\r?\n", raw):
        s = m.end()
        e = raw.find(b"endstream", s)
        if e < 0:
            continue
        seg = raw[s:e]
        try:
            seg = zlib.decompress(seg)
        except Exception:
            pass
        out += seg + b"\n"
    return bytes(out)


def obj(doc, xref):
    try:
        return doc.xref_object(xref, compressed=False)
    except Exception:
        return ""


def resolve_refs(s):
    """Every `N 0 R` reference in an object string, in order of appearance."""
    return [int(m.group(1)) for m in re.finditer(r"(\d+)\s+0\s+R", s or "")]


# --------------------------------------------------------------------------
# structure tree
# --------------------------------------------------------------------------

class Node:
    __slots__ = ("xref", "raw_type", "type", "kids", "alt", "actual",
                 "summary", "summary_in_A", "mcids", "parent")

    def __init__(self, xref, type_):
        self.xref = xref
        self.raw_type = type_
        self.type = type_        # set to the canonical role once the RoleMap is read
        self.kids = []
        self.alt = None
        self.actual = None
        self.summary = None
        self.summary_in_A = False
        self.mcids = []
        self.parent = None


def read_rolemap(doc, root_xref):
    """The document's own /RoleMap, as a raw-role -> standard-role dict.

    A PDF 2.0 tagged LaTeX document does not emit /H1 and /LI directly; it
    emits namespaced roles (`section`, `item`, `itemlabel`) and declares how
    they map. Testing the raw names instead reports zero headings and zero
    list items on a perfectly well-tagged file.
    """
    s = obj(doc, root_xref)
    m = re.search(r"/RoleMap\s+(\d+)\s+0\s+R", s)
    src = obj(doc, int(m.group(1))) if m else (
        re.search(r"/RoleMap\s*<<(.*?)>>", s, re.S).group(1) if "/RoleMap" in s else "")
    return {a: b for a, b in re.findall(r"/([A-Za-z0-9_.\-]+)\s*/([A-Za-z0-9_.\-]+)", src or "")}


def canon(role, rolemap, _depth=0):
    """Resolve a role through the RoleMap to its standard-structure name."""
    if _depth > 8 or role not in rolemap or rolemap[role] == role:
        return role
    return canon(rolemap[role], rolemap, _depth + 1)


def pdf_string(raw):
    """Decode a PDF literal or hex string into text."""
    if raw is None:
        return None
    raw = raw.strip()
    if raw.startswith("<") and not raw.startswith("<<"):
        h = re.sub(r"[^0-9A-Fa-f]", "", raw[1:-1])
        if len(h) % 2:
            h += "0"
        b = bytes.fromhex(h)
        if b[:2] in (b"\xfe\xff",):
            return b[2:].decode("utf-16-be", "replace")
        return b.decode("latin1", "replace")
    if raw.startswith("("):
        body = raw[1:-1]
        body = re.sub(r"\\([()\\])", r"\1", body)
        b = body.encode("latin1", "replace")
        if b[:2] == b"\xfe\xff":
            return b[2:].decode("utf-16-be", "replace")
        return b.decode("latin1", "replace")
    return raw


def build_tree(doc):
    """Walk /StructTreeRoot into Node objects, preserving kid order.

    Kid order *is* reading order — that is what makes the figure-position test
    meaningful, and it is exactly what a float breaks.
    """
    # Take the root from the catalog's /StructTreeRoot entry. Scanning objects
    # for the string instead finds the StructTreeRoot object itself and then
    # resolves whatever reference happens to follow the key -- which silently
    # yields an empty tree while every other test still runs.
    root_xref = None
    cat = obj(doc, doc.pdf_catalog())
    m = re.search(r"/StructTreeRoot\s+(\d+)\s+0\s+R", cat)
    if m:
        root_xref = int(m.group(1))
    else:
        for x in range(1, doc.xref_length()):
            if "/Type/StructTreeRoot" in obj(doc, x).replace(" ", ""):
                root_xref = x
                break
    if root_xref is None:
        return None, {}

    seen = {}

    def walk(xref, depth=0):
        if xref in seen or depth > 200:
            return seen.get(xref)
        s = obj(doc, xref)
        m = re.search(r"/S\s*/([A-Za-z0-9_.\-]+)", s)
        type_ = m.group(1) if m else ("StructTreeRoot" if depth == 0 else "?")
        n = Node(xref, type_)
        seen[xref] = n

        a = re.search(r"/Alt\s*(\([^\n]*?\)|<[0-9A-Fa-f\s]*>)", s)
        if a:
            n.alt = pdf_string(a.group(1))
        a = re.search(r"/ActualText\s*(\([^\n]*?\)|<[0-9A-Fa-f\s]*>)", s)
        if a:
            n.actual = pdf_string(a.group(1))
        a = re.search(r"/Summary\s*(\([^\n]*?\)|<[0-9A-Fa-f\s]*>)", s)
        if a:
            n.summary = pdf_string(a.group(1))

        # A bare top-level /Summary key (matched above) is not a valid PDF
        # structure-element key under ISO 32000 at all -- the spec's table
        # attributes (/RowSpan, /ColSpan, /Headers, /Scope, /Summary) live
        # inside /A with /O /Table, the same as /Scope does for TH. Check
        # that location specifically, resolving an indirect /A rather than
        # assuming an inline one, so this test cannot pass on a Summary that
        # sits somewhere a UA-1 reader will never look.
        a_m = re.search(r"/A\s*(\d+\s+0\s+R|<<.*?>>)", s, re.S)
        if a_m:
            a_body = a_m.group(1)
            ref_m = re.fullmatch(r"(\d+)\s+0\s+R", a_body)
            a_text = obj(doc, int(ref_m.group(1))) if ref_m else a_body
            if re.search(r"/O\s*/Table\b", a_text) and re.search(r"/Summary\s*[(<]", a_text):
                n.summary_in_A = True

        kids_m = re.search(r"/K\s*(\[.*?\]|\d+\s+0\s+R|<<.*?>>)", s, re.S)
        if kids_m:
            body = kids_m.group(1)
            # Integers directly under /K are MCIDs on the node's own page.
            # Strip the `N 0 R` references first: otherwise the generation
            # number 0 in every reference is counted as marked content 0.
            bare = re.sub(r"\d+\s+0\s+R", " ", body)
            for tok in re.finditer(r"(?<![\d.])(\d+)(?![\d.])", bare):
                n.mcids.append(int(tok.group(1)))
            for r in resolve_refs(body):
                kid = walk(r, depth + 1)
                if kid is not None and kid.type not in ("MCR", "OBJR"):
                    kid.parent = n
                    n.kids.append(kid)
                elif kid is not None and kid.type == "MCR":
                    mm = re.search(r"/MCID\s+(\d+)", obj(doc, r))
                    if mm:
                        n.mcids.append(int(mm.group(1)))
        return n

    root = walk(root_xref)
    rolemap = read_rolemap(doc, root_xref)
    for n in seen.values():
        n.type = canon(n.raw_type, rolemap)
    return root, rolemap


def linearize(root):
    """Depth-first reading-order sequence of nodes."""
    out = []

    def rec(n):
        out.append(n)
        for k in n.kids:
            rec(k)

    for k in root.kids:
        rec(k)
    return out


# --------------------------------------------------------------------------
# tests
# --------------------------------------------------------------------------

HEADING_RE = re.compile(r"^H([1-9])?$")

# A PDF name may contain hyphens and dots, and the LaTeX tagging namespace uses
# them heavily: /section-number, /text-unit, /theorem-like. Matching only \w+
# skips those BDC operators entirely, which both orphans the text inside them
# and unbalances the EMC stack -- reporting phantom unreachable operators in a
# document that is correctly tagged.
NAME = r"[A-Za-z0-9_.\-]+"
MC_OP_RE = (
    rf"/({NAME})\s*(<<(?:[^<>]|<<[^<>]*>>)*>>)\s*BDC"   # inline property dict
    rf"|/({NAME})\s*/({NAME})\s*BDC"                     # named property list
    rf"|/({NAME})\s+BMC"
    r"|\bEMC\b|\bTJ\b|\bTj\b"
)


def test_headings(order, expected):
    hs = [n for n in order if HEADING_RE.match(n.type)]
    levels = [int(HEADING_RE.match(n.type).group(1) or 1) for n in hs]
    skipped = []
    prev = 0
    for i, lv in enumerate(levels):
        if prev and lv > prev + 1:
            skipped.append((i, prev, lv))
        prev = lv
    ok = (expected is None or len(hs) == expected) and not skipped
    return {
        "count": len(hs),
        "expected": expected,
        "by_level": dict(Counter(f"H{l}" for l in levels)),
        "skipped_levels": skipped,
        "pass": ok,
    }


def test_reachability(doc, order):
    """Every text-showing operator: artifact, reachable, or orphaned.

    Marked content nests, and the two nesting rules are not symmetric:

    * An /Artifact frame governs everything inside it. Nesting a tagged span
      within an artifact does not rescue that span -- to assistive technology
      the whole region is decoration. So artifact wins if it appears ANYWHERE
      in the enclosing stack.
    * Otherwise reachability is decided by the nearest enclosing frame that
      carries an MCID, not the innermost frame, because an accsupp
      /ActualText span sits inside the Formula that owns the MCID and carries
      no MCID of its own.

    Resolving only to the innermost non-null frame -- the obvious
    implementation -- silently reports artifacted content as reachable, which
    is how six boxed equations can be decoration while the count reads zero.
    """
    referenced = set()
    for n in order:
        referenced |= set(n.mcids)
    # MCIDs may also be reached through /MCR dictionaries anywhere in the file.
    for x in range(1, doc.xref_length()):
        s = obj(doc, x)
        if "/MCR" in s or "/StructElem" in s:
            referenced |= {int(m.group(1)) for m in re.finditer(r"/MCID\s+(\d+)", s)}

    total = artifact = unreachable = 0
    orphan_pages = Counter()
    for pno, page in enumerate(doc, 1):
        try:
            cs = page.read_contents().decode("latin1")
        except Exception:
            continue
        stack = []
        for m in re.finditer(MC_OP_RE, cs):
            tok = m.group(0)
            if tok.endswith("BDC"):
                tag = m.group(1) or m.group(3)
                props = m.group(2) or ""
                mc = re.search(r"/MCID\s+(\d+)", props)
                if tag == "Artifact":
                    stack.append("A")
                else:
                    stack.append(int(mc.group(1)) if mc else None)
            elif tok.endswith("BMC"):
                stack.append("A" if m.group(5) == "Artifact" else None)
            elif tok == "EMC":
                if stack:
                    stack.pop()
            else:
                total += 1
                if "A" in stack:
                    artifact += 1
                    continue
                frame = None
                for fr in reversed(stack):
                    if fr is not None:
                        frame = fr
                        break
                if not (isinstance(frame, int) and frame in referenced):
                    unreachable += 1
                    orphan_pages[pno] += 1
    return {
        "total_ops": total,
        "artifact_ops": artifact,
        "reachable_ops": total - artifact - unreachable,
        "unreachable_ops": unreachable,
        "orphans_by_page": dict(orphan_pages),
        "pass": unreachable == 0,
    }


def test_artifacts(doc):
    """What got marked as decoration, and whether any of it looks meaningful.

    Page furniture (numbers, rules) belongs here. A word does not: in the
    reference run an artifacted table cell deleted 'Quantum' from a
    Classical/Quantum comparison and inverted the passage.
    """
    suspicious = []
    buried = []
    counts = Counter()
    for pno, page in enumerate(doc, 1):
        try:
            cs = page.read_contents().decode("latin1")
        except Exception:
            continue
        # Walk properly: an artifact frame can contain nested marked content,
        # so the region ends at its *matching* EMC, not the first one.
        depth = 0
        art_start = None
        for m in re.finditer(MC_OP_RE, cs):
            tok = m.group(0)
            if tok.endswith("BDC") or tok.endswith("BMC"):
                tag = m.group(1) or m.group(3) or m.group(5)
                if art_start is None and tag == "Artifact":
                    art_start = (m.end(), m.group(2) or "")
                    depth = 1
                elif art_start is not None:
                    depth += 1
            elif tok == "EMC" and art_start is not None:
                depth -= 1
                if depth == 0:
                    body = cs[art_start[0]:m.start()]
                    props = art_start[1]
                    sub = re.search(r"/Subtype\s*/(\w+)", props)
                    counts[sub.group(1) if sub else "unclassified"] += 1
                    # Strings inside nested property dictionaries are metadata,
                    # not painted text; strip them before reading the body, or
                    # every /ActualText fallback reads as artifacted content.
                    clean = re.sub(r"<<(?:[^<>]|<<[^<>]*>>)*>>", " ", body)
                    text = "".join(
                        re.sub(r"\\[()\\]", "", t.group(1))
                        for t in re.finditer(r"\(((?:[^()\\]|\\.)*)\)", clean)
                    )
                    # A tagged LuaLaTeX PDF shows text as hex CID strings, not
                    # as literals, so a scan for `(...)` alone finds nothing to
                    # object to no matter what has been artifacted. Decode the
                    # hex form too: CIDs are not Unicode, but a run of them is
                    # still evidence that glyphs -- not page furniture -- were
                    # marked as decoration.
                    hexruns = re.findall(r"<([0-9A-Fa-f\s]{8,})>\s*(?:TJ|Tj|\])", clean)
                    glyphs = sum(len(re.sub(r"\s", "", h)) // 4 for h in hexruns)
                    words = re.findall(r"[A-Za-z]{4,}", text)
                    if glyphs >= 6:
                        words = words + [f"<{glyphs} glyphs shown as hex CIDs>"]
                    if words:
                        suspicious.append({"page": pno,
                                           "subtype": sub.group(1) if sub else None,
                                           "text": text[:120], "words": words[:8]})
                    # Tagged structure nested inside decoration is content the
                    # author meant to expose and the reader will never hear.
                    inner = re.findall(r"/(" + NAME + r")\s*<<[^<>]*/MCID", body)
                    if inner:
                        buried.append({"page": pno, "tags": sorted(set(inner))})
                    art_start = None
    return {
        "artifact_frames": sum(counts.values()),
        "by_subtype": dict(counts),
        "suspicious": suspicious,
        "tagged_content_inside_artifact": buried,
        "pass": not suspicious and not buried,
    }


def test_figure_positions(order):
    figs = [i for i, n in enumerate(order) if n.type == "Figure"]
    n = len(order) or 1
    pos = [round(100.0 * i / n, 1) for i in figs]
    # A figure is "clustered at the end" if it sits past 90% of reading order
    # while the document has body content after it -- the float symptom.
    tail = [p for p in pos if p > 90.0]
    clustered = len(tail) >= 2 or (len(figs) and len(tail) == len(figs) and len(figs) > 1)
    return {
        "figure_count": len(figs),
        "positions_pct": pos,
        "past_90pct": tail,
        "pass": not clustered,
    }


def test_lists_tables(order):
    c = Counter(n.type for n in order)
    li_bad = []
    for n in order:
        if n.type == "LI":
            kinds = {k.type for k in n.kids}
            if not ({"Lbl"} <= kinds and {"LBody"} <= kinds):
                li_bad.append({"xref": n.xref, "children": sorted(kinds)})
    tables_no_th = []
    tables_no_summary = []
    tables_summary_not_in_A = []
    for n in order:
        if n.type == "Table":
            def has_th(x):
                return x.type == "TH" or any(has_th(k) for k in x.kids)
            if not has_th(n):
                tables_no_th.append(n.xref)
            # /Summary must sit on the Table itself, not on a child TH. A
            # count of /Summary keys anywhere in the file is not this test.
            if not (n.summary or "").strip():
                tables_no_summary.append(n.xref)
            # Presence of a /Summary key anywhere on the object is not the
            # same as a spec-valid one: ISO 32000's table attributes (this
            # one included) are defined inside /A with /O /Table, not as a
            # bare top-level StructElem key. A checker reading only valid
            # locations (PAC 2026 confirmed to be one, 2026-08-20) sees a
            # table with no Summary at all if this fails, regardless of
            # tables_no_summary above.
            if (n.summary or "").strip() and not n.summary_in_A:
                tables_summary_not_in_A.append(n.xref)
    tr_bad = []
    for n in order:
        if n.type == "TR":
            p = n.parent.type if n.parent else None
            if p not in ("Table", "THead", "TBody", "TFoot"):
                tr_bad.append({"xref": n.xref, "parent": p})
    return {
        "counts": {k: c.get(k, 0) for k in
                   ("L", "LI", "Lbl", "LBody", "Table", "TR", "TH", "TD",
                    "THead", "TBody", "TFoot")},
        "LI_missing_child": li_bad,
        "tables_without_TH": tables_no_th,
        "tables_without_summary": tables_no_summary,
        "tables_summary_not_in_A": tables_summary_not_in_A,
        "TR_bad_parent": tr_bad,
        "pass": not li_bad and not tables_no_th and not tr_bad
                and not tables_no_summary and not tables_summary_not_in_A,
    }


def mathml_streams(doc):
    """The MathML attached to Formula elements, read from the /AF files.

    The MathML is not in the page content: it is an EmbeddedFile of subtype
    application/mathml+xml associated with each Formula. Scanning the
    concatenated page streams for `<math` therefore inspects the wrong bytes
    and reports whatever it happens to find.
    """
    out = []
    for x in range(1, doc.xref_length()):
        s = obj(doc, x)
        if "mathml" not in s.lower():
            continue
        try:
            data = doc.xref_stream(x)
        except Exception:
            continue
        if data and b"<math" in data:
            out.append((x, data.decode("utf-8", "replace")))
    # Some producers put the MathML in the stream without naming it in the dict.
    if not out:
        for x in range(1, doc.xref_length()):
            try:
                data = doc.xref_stream(x)
            except Exception:
                continue
            if data and b"<math" in data:
                out.append((x, data.decode("utf-8", "replace")))
    return out


def mathml_is_empty(frag):
    """True if a MathML fragment carries no recoverable mathematics.

    A boxed equation exports a well-formed shell -- <math>, <mtable>, an
    equation-label <mtext> -- whose only actual content is U+FFFD. Testing for
    the presence of a token element passes it, because <mtext> is a token
    element. What matters is whether anything is left after the label and the
    replacement characters are removed.
    """
    body = re.sub(r"<mtext[^>]*intent=\":equation-label\"[^>]*>.*?</mtext>", " ",
                  frag, flags=re.S)
    body = re.sub(r"<mtext[^>]*>\s*\(\s*\d+\s*\)\s*</mtext>", " ", body, flags=re.S)
    # Strip the tags and see what character content is left. Test for ANY
    # non-space character rather than for a named range: mathematics is set in
    # mathematical-italic codepoints (U+1D400 and up), and a rule that lists
    # ASCII and Greek reports every single-symbol formula as empty.
    text = re.sub(r"<[^>]+>", " ", body).replace("�", " ")
    if text.strip():
        return False
    # No literal content: is there any structural math element that carries
    # meaning on its own (a fraction, a root, a script)?
    return not re.search(r"<(mfrac|msqrt|mroot|msup|msub|msubsup|munderover)\b", body)


def mathml_for_formula(doc, n):
    """The MathML attached to one Formula element, via its /AF files.

    Returns (embedded-file xref, fragment) or (None, None). Scanning every
    MathML file in the PDF and then comparing *counts* against spoken
    Formula elements is not this function -- that is how an empty Formula
    with no fallback was reported as covered by a different equation's
    spoken rendition.
    """
    s = obj(doc, n.xref)
    af = re.search(r"/AF\s*\[(.*?)\]", s, re.S)
    refs = resolve_refs(af.group(1)) if af else resolve_refs(s)
    seen = set()
    queue = list(refs)
    while queue:
        r = queue.pop(0)
        if r in seen:
            continue
        seen.add(r)
        try:
            data = doc.xref_stream(r)
        except Exception:
            data = None
        if data and b"<math" in data:
            return r, data.decode("utf-8", "replace")
        fs = obj(doc, r)
        if "mathml" in fs.lower() or "/EF" in fs or "/F" in fs:
            queue.extend(x for x in resolve_refs(fs) if x not in seen)
    return None, None


def test_math(doc, order):
    """Formula tagging, and whether every equation carries its meaning.

    A box (and some stroke macros) defeat the MathML generator: the fragment
    comes out as a shell holding the equation number and a replacement
    character. That is a toolchain limitation, so the acceptance rule is not
    "no empty MathML" -- it is that every Formula whose MathML is empty is
    identified, and THAT SAME Formula carries /ActualText or /Alt. A count
    comparison of empty files vs spoken Formulas is not this test.
    """
    formulas = [n for n in order if n.type == "Formula"]
    empty, spoken_on_empty, uncovered = [], [], []
    frags = []
    repl = 0
    for n in formulas:
        xref, frag = mathml_for_formula(doc, n)
        if frag is None:
            continue
        frags.append((n.xref, xref, frag))
        repl += frag.count("�")
        if mathml_is_empty(frag):
            empty.append(n.xref)
            if n.actual or n.alt:
                spoken_on_empty.append({
                    "formula_xref": n.xref,
                    "mathml_xref": xref,
                    "spoken": (n.actual or n.alt or "")[:70],
                })
            else:
                uncovered.append({
                    "formula_xref": n.xref,
                    "mathml_xref": xref,
                })
    spoken = [n for n in formulas if n.actual or n.alt]
    return {
        "formula_elements": len(formulas),
        "mathml_attached_files": len({x for _, x, _ in frags}),
        "mathml_empty": len(empty),
        "mathml_empty_xrefs": empty[:40],
        "empty_with_fallback": spoken_on_empty,
        "empty_without_fallback": uncovered,
        "formulas_with_alt_or_actualtext": len(spoken),
        "spoken_fallbacks": [(n.xref, (n.actual or n.alt or "")[:70])
                             for n in spoken],
        "replacement_chars_in_mathml": repl,
        "pass": len(formulas) > 0 and len(frags) > 0 and not uncovered,
    }


def test_alt(order, altfile):
    figs = [n for n in order if n.type == "Figure"]
    missing = [n.xref for n in figs if not (n.alt or "").strip()]
    generic_re = re.compile(
        r"^\s*(figure|diagram|image|picture|graph|graphic|a diagram|an image"
        r"|image of a graph|plot|chart)\s*\.?\s*$", re.I)
    generic = [n.alt for n in figs if n.alt and generic_re.match(n.alt)]
    sidecar_ok, sidecar_missing = None, []
    if altfile:
        try:
            side = json.load(open(altfile))
        except Exception as e:
            side = None
            sidecar_ok = f"unreadable: {e}"
        if side:
            wanted = {v.strip() for v in side.values() if isinstance(v, str)}
            have = {(n.alt or "").strip() for n in figs}
            sidecar_missing = sorted(w[:60] for w in wanted - have)
            sidecar_ok = not sidecar_missing
    return {
        "figures": len(figs),
        "with_alt": len(figs) - len(missing),
        "missing_alt": missing,
        "generic_alt": generic,
        "sidecar_match": sidecar_ok,
        "sidecar_missing": sidecar_missing,
        "pass": not missing and not generic,
    }


def test_metadata(doc, path, blob):
    """Language, title, DisplayDocTitle and the PDF/UA identifier.

    All of these live in objects that may sit inside an object stream, so they
    are read through the xref table; a raw byte scan of the file reports them
    absent on any compressed PDF -- including every one this pipeline builds.
    """
    md = doc.metadata or {}
    cat = obj(doc, doc.pdf_catalog())

    lang_m = re.search(r"/Lang\s*(\([^)]*\)|<[0-9A-Fa-f\s]*>)", cat)
    lang = pdf_string(lang_m.group(1)) if lang_m else None

    disp = False
    vp = re.search(r"/ViewerPreferences\s+(\d+)\s+0\s+R", cat)
    vp_src = obj(doc, int(vp.group(1))) if vp else cat
    if re.search(r"/DisplayDocTitle\s+true", vp_src):
        disp = True

    # The PDF/UA identifier lives in the XMP metadata stream.
    xmp = ""
    mm = re.search(r"/Metadata\s+(\d+)\s+0\s+R", cat)
    if mm:
        try:
            xmp = doc.xref_stream(int(mm.group(1))).decode("utf-8", "replace")
        except Exception:
            xmp = ""
    ua_part = re.search(r"pdfuaid[:\s]*part[^0-9]*(\d+)", xmp, re.I) \
        or re.search(rb"pdfuaid[:\s]*part[^0-9]*(\d+)", blob, re.I)
    ua = bool(ua_part)

    return {
        "title": md.get("title") or None,
        "lang": lang,
        "DisplayDocTitle": disp,
        "pdfuaid_part": (ua_part.group(1).decode() if isinstance(ua_part.group(1), bytes)
                         else ua_part.group(1)) if ua_part else None,
        "encrypted": doc.is_encrypted,
        "permissions_int": doc.permissions,
        "pass": bool(md.get("title")) and bool(lang) and disp and ua and not doc.is_encrypted,
    }


def test_full_text(doc):
    """MDAS item 3: the document has real text, not just page images."""
    chars = sum(len(p.get_text().strip()) for p in doc)
    return {"extracted_chars": chars, "pass": chars > 200}


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--alt", default=None, help="alt_text.json sidecar")
    ap.add_argument("--sections", type=int, default=None,
                    help="expected heading count from the .tex outline")
    ap.add_argument("--json", default=None, help="write full results here")
    a = ap.parse_args()

    doc = fitz.open(a.pdf)
    blob = all_streams(a.pdf)
    root, rolemap = build_tree(doc)
    if root is None:
        print("FAIL: no /StructTreeRoot -- the PDF is untagged. This is a failed run.")
        sys.exit(2)
    order = linearize(root)

    R = {
        "pdf": a.pdf,
        "pages": doc.page_count,
        "structure_elements": len(order),
        "element_types": dict(Counter(n.type for n in order).most_common()),
        "raw_element_types": dict(Counter(n.raw_type for n in order).most_common()),
        "rolemap_entries": len(rolemap),
        "t1_headings": test_headings(order, a.sections),
        "t2_reachability": test_reachability(doc, order),
        "t3_artifacts": test_artifacts(doc),
        "t4_figure_positions": test_figure_positions(order),
        "lists_tables": test_lists_tables(order),
        "math": test_math(doc, order),
        "alt_text": test_alt(order, a.alt),
        "metadata": test_metadata(doc, a.pdf, blob),
        "full_text": test_full_text(doc),
    }

    def line(key, label, detail):
        r = R[key]
        print(f"[{'PASS' if r['pass'] else 'FAIL'}] {label:<34} {detail(r)}")

    print(f"=== {a.pdf} — {R['pages']} pages, {R['structure_elements']} structure elements ===")
    print(f"roles normalized through the document RoleMap ({R['rolemap_entries']} entries)")
    print("element types:", R["element_types"])
    print()
    print("--- Step 4d mandatory numeric tests ---")
    line("t1_headings", "1. heading inventory",
         lambda r: f"{r['count']} H-elements (expected {r['expected']}) {r['by_level']}"
                   + (f" SKIPPED LEVELS {r['skipped_levels']}" if r['skipped_levels'] else ""))
    line("t2_reachability", "2. content reachability (MCID)",
         lambda r: f"{r['unreachable_ops']} unreachable of {r['total_ops']} "
                   f"({r['artifact_ops']} decoration, {r['reachable_ops']} reachable)"
                   + (f" pages {r['orphans_by_page']}" if r['orphans_by_page'] else ""))
    line("t3_artifacts", "3. artifact audit",
         lambda r: f"{r['artifact_frames']} frames {r['by_subtype']}; "
                   f"{len(r['suspicious'])} carry words; "
                   f"{len(r['tagged_content_inside_artifact'])} bury tagged content")
    line("t4_figure_positions", "4. figure reading position",
         lambda r: f"{r['figure_count']} figures at {r['positions_pct']}%")
    print()
    print("--- supporting checks ---")
    line("lists_tables", "list/table structure",
         lambda r: f"{r['counts']}; tables without /Summary: {r['tables_without_summary']}; "
                   f"/Summary not in /A (spec-invalid location): {r['tables_summary_not_in_A']}")
    line("math", "math tagging + MathML",
         lambda r: f"{r['formula_elements']} Formula, {r['mathml_attached_files']} MathML files, "
                   f"{r['mathml_empty']} empty, "
                   f"{len(r['empty_without_fallback'])} empty without a fallback on that Formula, "
                   f"{r['formulas_with_alt_or_actualtext']} carry a spoken fallback")
    line("alt_text", "alt text",
         lambda r: f"{r['with_alt']}/{r['figures']} figures; sidecar match: {r['sidecar_match']}")
    line("metadata", "metadata",
         lambda r: f"title={r['title']!r} lang={r['lang']!r} "
                   f"DisplayDocTitle={r['DisplayDocTitle']} pdfuaid-part={r['pdfuaid_part']}")
    line("full_text", "full text present (MDAS 3)", lambda r: f"{r['extracted_chars']} chars")

    if R["t3_artifacts"]["suspicious"]:
        print("\n  artifacted content carrying words (inspect each):")
        for s in R["t3_artifacts"]["suspicious"][:10]:
            print(f"    p{s['page']}: {s['words']}")
    if R["math"]["mathml_empty"]:
        print("\n  equations whose MathML is empty (a box or stroke can defeat")
        print("  the generator). Each must carry a spoken rendition on THAT")
        print("  Formula element, not merely somewhere in the document:")
        for item in R["math"]["empty_with_fallback"]:
            print(f"    xref {item['formula_xref']}: \"{item['spoken']}...\"")
        for item in R["math"]["empty_without_fallback"]:
            print(f"    xref {item['formula_xref']}: NO FALLBACK (MathML file {item['mathml_xref']})")
    if R["t3_artifacts"]["tagged_content_inside_artifact"]:
        print("\n  tagged content buried inside an /Artifact (unreadable by AT):")
        for s in R["t3_artifacts"]["tagged_content_inside_artifact"][:10]:
            print(f"    p{s['page']}: {s['tags']}")
    if R["alt_text"]["sidecar_missing"]:
        print("\n  sidecar alt strings not found in the PDF:")
        for s in R["alt_text"]["sidecar_missing"]:
            print(f"    {s}...")

    if a.json:
        json.dump(R, open(a.json, "w"), indent=1)
        print(f"\nwrote {a.json}")

    failed = [k for k in ("t1_headings", "t2_reachability", "t3_artifacts",
                          "t4_figure_positions", "lists_tables", "math",
                          "alt_text", "metadata", "full_text") if not R[k]["pass"]]
    print(f"\n{'ALL CHECKS PASS' if not failed else 'FAILED: ' + ', '.join(failed)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
