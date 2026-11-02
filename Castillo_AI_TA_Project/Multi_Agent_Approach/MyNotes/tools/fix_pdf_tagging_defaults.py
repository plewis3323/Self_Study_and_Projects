#!/usr/bin/env python3
"""
Patch tagging defects that trace back to the toolchain, not the document.
Defects 1-2 were surfaced by a PAC 2026 detailed report against the
2026-08-20 build (md5 f6e5c207...); defect 3 was found investigating why
PAC's Run 2 (md5 b92b19d2...) still flagged 100% of Tables and Lists after
1-2 were already fixed.

1. RoleMap /text-unit -> /Part and /float -> /Note. Both are latex-lab's own
   built-in default table for the pdf2/UA-2 namespace (tagpdf-ns-latex-lab.def:
   "text-unit, Part, pdf2," / "float, Aside, pdf2," -> Aside resolves to Note),
   not something goldsteinnotes.sty or the transcription chose. Every ordinary
   paragraph is wrapped as text-unit (57 of them here), and every LaTeX float
   environment (5 figures + 3 tables = 8) is wrapped as float -- so every
   paragraph in the document registers as a /Part (a role meant for top-level
   book divisions) and every figure/table sits inside a /Note wrapper. PAC
   flags both as "possibly inappropriate use". Remap text-unit -> /P (this
   document already role-maps plain "text" -> /P, so a paragraph wrapper
   landing on the same standard tag is the correct fix) and float -> /Div
   (a semantically neutral generic container, already used elsewhere in this
   RoleMap for /Div).

2. Table header cells carry /C /TH-col, which resolves via this document's
   own /ClassMap to <</O /Table /Scope /Column>> -- a fully spec-conformant
   ISO 32000-2 attribute-class indirection, and the mechanism
   Multi_Agent_Outline.md deliberately chose (Step 4b) specifically because a
   checker that only looks for a *direct* /Scope key false-negatives here.
   PAC's "Table header cell has no associated data cells" check flags all 7/7
   TH cells in this document -- exactly that false-negative, consistent with
   PAC 2026's own "this document is PDF 2.0; results may be unreliable"
   warning. Add a literal /A duplicating the ClassMap's resolved dict directly
   on each TH element, redundant with /C but readable by a checker that never
   resolves ClassMap at all.

3. Table /Summary was written as a bare top-level /Summary key on the Table
   StructElem dict -- not a valid PDF structure-element key under ISO 32000
   at all (the spec's own Table attributes -- /RowSpan, /ColSpan, /Headers,
   /Scope, /Summary -- live inside the /A attribute dictionary with
   /O /Table, exactly like /Scope does for TH above). goldsteinnotes.sty's
   own comment admits this: "this kernel offers no documented key for it --
   so it is written onto the Table structure directly." check_structure.py's
   own table_summary test only checked presence of that key anywhere on the
   element, so this was never caught. From a strict UA-1 reader's
   perspective every Table in this document has NO valid Summary attribute
   at all, which plausibly explains PAC flagging 3/3 Tables as "possibly
   inappropriate use" regardless of size or content. Fix: add a proper
   /A << /O /Table /Summary (same text) >> to each Table, additive
   alongside the existing non-standard key (harmless, ignored by
   spec-compliant readers, left in place rather than risk breaking anything
   that reads it).

4. List (enumerate) elements carry /C /enumerate, which resolves via
   /ClassMap to <</O /List /ListNumbering /Ordered>> -- the same ClassMap-
   only-attribute pattern as TH/Scope in (2). PAC flags 2/2 Lists as
   "possibly inappropriate use" regardless of item count (2-item and 4-item
   lists both flagged). Add a literal /A duplicating the resolved dict, same
   fix as (2), applied to L instead of TH.

5. Formula elements carry /C /display or /inline, resolving via /ClassMap to
   a Layout/Placement dict. Both classes use the identical mechanism, but
   PAC flags 52/52 display and 0/146 inline -- so an unresolved-ClassMap
   theory does NOT explain this split (it would affect both equally). Not
   fixed here for that reason (tested and rejected, see PIPELINE_LOG.md);
   listed for completeness so a future run does not re-investigate the same
   dead end.

All four applied fixes are additive/redirective -- no content, reading
order, or MCID is touched -- and are identity-matched against the actual
struct tree rather than assumed from a fixed count.

Usage:
    python3 fix_pdf_tagging_defaults.py DOC.pdf --out OUT.pdf
    python3 fix_pdf_tagging_defaults.py DOC.pdf --in-place
"""

import argparse
import sys

import pikepdf


def fix_rolemap(pdf):
    st = pdf.Root.StructTreeRoot
    rm = st.get("/RoleMap", None)
    if rm is None:
        sys.exit("no /RoleMap in StructTreeRoot -- nothing to fix")

    changes = []
    remap = {"/text-unit": "/P", "/float": "/Div"}
    for tag, new_role in remap.items():
        if tag not in rm:
            sys.exit(f"expected RoleMap entry {tag} not present -- shape changed, refusing to guess")
        old_role = str(rm[tag])
        if old_role == new_role:
            changes.append((tag, old_role, new_role, "already fixed"))
            continue
        rm[tag] = pikepdf.Name(new_role)
        changes.append((tag, old_role, new_role, "rewritten"))
    return changes


def fix_th_scope(pdf):
    st = pdf.Root.StructTreeRoot
    cm = st.get("/ClassMap", None)
    if cm is None or "/TH-col" not in cm:
        sys.exit("no /ClassMap /TH-col entry -- shape changed, refusing to guess")
    scope_dict = dict(cm["/TH-col"])  # {'/O': '/Table', '/Scope': '/Column'}

    fixed, already, skipped = [], [], []
    for obj in pdf.objects:
        try:
            is_th = obj.get("/Type") == pikepdf.Name("/StructElem") and obj.get("/S") == pikepdf.Name("/TH")
        except Exception:
            continue
        if not is_th:
            continue
        existing_a = obj.get("/A", None)
        if existing_a is not None:
            already.append(obj.objgen)
            continue
        cls = obj.get("/C", None)
        if cls is None or str(cls) != "/TH-col":
            skipped.append((obj.objgen, str(cls)))
            continue
        a = pdf.make_indirect(pikepdf.Dictionary(scope_dict))
        obj["/A"] = a
        fixed.append(obj.objgen)
    return fixed, already, skipped


def fix_table_summary_attr(pdf):
    fixed, already, skipped = [], [], []
    for obj in pdf.objects:
        try:
            is_table = obj.get("/Type") == pikepdf.Name("/StructElem") and obj.get("/S") == pikepdf.Name("/Table")
        except Exception:
            continue
        if not is_table:
            continue
        existing_a = obj.get("/A", None)
        if existing_a is not None:
            already.append(obj.objgen)
            continue
        summary = obj.get("/Summary", None)
        if summary is None:
            skipped.append(obj.objgen)
            continue
        a = pdf.make_indirect(pikepdf.Dictionary({"/O": pikepdf.Name("/Table"), "/Summary": summary}))
        obj["/A"] = a
        fixed.append(obj.objgen)
    return fixed, already, skipped


def fix_list_numbering(pdf):
    st = pdf.Root.StructTreeRoot
    cm = st.get("/ClassMap", None)
    if cm is None or "/enumerate" not in cm:
        sys.exit("no /ClassMap /enumerate entry -- shape changed, refusing to guess")
    numbering_dict = dict(cm["/enumerate"])  # {'/O': '/List', '/ListNumbering': '/Ordered'}

    fixed, already, skipped = [], [], []
    for obj in pdf.objects:
        try:
            is_l = obj.get("/Type") == pikepdf.Name("/StructElem") and obj.get("/S") == pikepdf.Name("/enumerate")
        except Exception:
            continue
        if not is_l:
            continue
        existing_a = obj.get("/A", None)
        if existing_a is not None:
            already.append(obj.objgen)
            continue
        a = pdf.make_indirect(pikepdf.Dictionary(numbering_dict))
        obj["/A"] = a
        fixed.append(obj.objgen)
    return fixed, already, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--out")
    ap.add_argument("--in-place", action="store_true")
    args = ap.parse_args()

    if not args.out and not args.in_place:
        sys.exit("give --out OUT.pdf or --in-place")
    out_path = args.pdf if args.in_place else args.out

    pdf = pikepdf.open(args.pdf, allow_overwriting_input=args.in_place)

    rolemap_changes = fix_rolemap(pdf)
    th_fixed, th_already, th_skipped = fix_th_scope(pdf)
    table_fixed, table_already, table_skipped = fix_table_summary_attr(pdf)
    list_fixed, list_already, list_skipped = fix_list_numbering(pdf)

    if len(th_fixed) + len(th_already) != 7:
        sys.exit(f"expected 7 TH cells total, found {len(th_fixed)} fixed + {len(th_already)} already-set "
                  f"({len(th_skipped)} skipped: {th_skipped}). Shape changed -- refusing to save.")
    if len(table_fixed) + len(table_already) + len(table_skipped) != 3:
        sys.exit(f"expected 3 Table elements total, found {len(table_fixed)} fixed + {len(table_already)} "
                  f"already-set + {len(table_skipped)} skipped (no /Summary key). Shape changed -- refusing to save.")
    if table_skipped:
        sys.exit(f"{len(table_skipped)} Table element(s) have no /Summary key to promote into /A: {table_skipped}. "
                  f"Shape changed -- refusing to guess.")
    if len(list_fixed) + len(list_already) != 2:
        sys.exit(f"expected 2 List (enumerate) elements total, found {len(list_fixed)} fixed + "
                  f"{len(list_already)} already-set ({len(list_skipped)} skipped). Shape changed -- refusing to save.")

    pdf.save(out_path)
    print(f"wrote {out_path}")
    print("RoleMap:")
    for tag, old, new, status in rolemap_changes:
        print(f"  {tag}: {old} -> {new}  ({status})")
    print(f"TH /Scope: {len(th_fixed)} cells given a direct /A (already set: {len(th_already)})")
    if th_skipped:
        print(f"  ({len(th_skipped)} TH cells skipped, unexpected /C: {th_skipped})")
    print(f"Table /Summary: {len(table_fixed)} tables given a proper /A << /O /Table /Summary >> "
          f"(already set: {len(table_already)})")
    print(f"List /ListNumbering: {len(list_fixed)} lists given a direct /A (already set: {len(list_already)})")


if __name__ == "__main__":
    main()
