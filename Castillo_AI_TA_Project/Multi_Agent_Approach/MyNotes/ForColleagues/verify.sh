#!/usr/bin/env bash
# Re-run every acceptance check on the worked-example PDF and print the numbers.
#
# Nothing here trusts a stored report. A conformance pass alone is a floor:
# in the 13 August reference run a checker passed cleanly three times while
# 16 headings were mis-tagged and 24 content operators sat outside the tag
# tree. The numeric tests are the acceptance criteria.
#
#   ./verify.sh [path/to/verapdf]
#   ./verify.sh --reproduce        re-derive Stage 1 from the source PDF and
#                                  compare pixel by pixel (no LaTeX needed)
#
# Requires: python3 with pymupdf, numpy, pillow. veraPDF is optional but
# strongly recommended; its absence is reported rather than skipped silently.
# --reproduce additionally wants pdftoppm (poppler-utils).

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

find_one() {
  for p in "$@"; do [ -e "$p" ] && { echo "$p"; return; }; done
}

# --- ./verify.sh --reproduce -------------------------------------------------
# The deliverable's md5 proves the file you were sent is the file that was
# audited. It says nothing about whether the pipeline that produced it still
# works. This does: it re-renders the source PDF, re-cuts the segments with the
# recorded invocation, re-cuts the figures from the recorded boxes, and demands
# they come back identical to the frozen ones. Stage 1 is deterministic, so
# anything other than "identical" means the kit or the toolchain has drifted.
if [ "${1:-}" = "--reproduce" ]; then
  EX="$HERE/Worked_Example"
  SRC="$EX/Input/Lecture-scattering-Hamiltonian_241022-forward.pdf"
  WORK="${TMPDIR:-/tmp}/kit_reproduce_$$"
  trap 'rm -rf "$WORK"' EXIT
  mkdir -p "$WORK"

  command -v pdftoppm >/dev/null || {
    echo "FATAL: pdftoppm not found (install poppler-utils). PyMuPDF renders"
    echo "the same pages differently and the comparison would fail spuriously."
    exit 2; }

  echo "=============================================================="
  echo " Reproducing Stage 1 from $(basename "$SRC")"
  echo "=============================================================="
  python3 "$HERE/tools/render_pages.py" "$SRC" "$WORK/pages" --dpi 300 || exit 2
  python3 "$HERE/tools/render_pages.py" "$SRC" "$WORK/pages600" --dpi 600 --pages 2 || exit 2

  echo
  echo "--- page rasters vs the frozen ones ---"
  python3 - "$WORK/pages" "$EX/Intermediate/pages" <<'PY' || RC=1
import sys, glob, os
import numpy as np
from PIL import Image
mine, frozen = sys.argv[1], sys.argv[2]
bad = 0
for p in sorted(glob.glob(os.path.join(mine, "page-*.png"))):
    q = os.path.join(frozen, os.path.basename(p))
    if not os.path.exists(q):
        print(f"  [MISS] {os.path.basename(p)}"); bad += 1; continue
    a = np.asarray(Image.open(p).convert("RGB"))
    b = np.asarray(Image.open(q).convert("RGB"))
    same = a.shape == b.shape and np.array_equal(a, b)
    print(f"  [{'SAME' if same else 'DIFF'}] {os.path.basename(p)}  {a.shape[1]}x{a.shape[0]}")
    bad += 0 if same else 1
sys.exit(1 if bad else 0)
PY

  echo
  echo "--- segments, re-cut with the recorded invocation ---"
  INV=$(python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))['invocation']
print(d['target'],d['overlap'],d['min_h'],d['pad_top'],d['protect'])
" "$EX/Intermediate/segment_run.json")
  set -- $INV
  TGT=$1; OVL=$2; MINH=$3; PADT=$4; shift 4; PROT="$*"
  python3 "$HERE/tools/segment_seams.py" "$WORK/pages/page-*.png" "$WORK/segs" \
      --target "$TGT" --overlap "$OVL" --min-h "$MINH" --pad-top "$PADT" \
      --protect "$PROT" | tail -6
  python3 - "$WORK/segs" "$EX/Intermediate/segments" <<'PY' || RC=1
import sys, glob, os
import numpy as np
from PIL import Image
mine, frozen = sys.argv[1], sys.argv[2]
got = sorted(os.path.basename(p) for p in glob.glob(os.path.join(mine, "page*_seg*.png")))
want = sorted(os.path.basename(p) for p in glob.glob(os.path.join(frozen, "page*_seg*.png")))
if got != want:
    print(f"  [DIFF] segment list: {len(got)} cut, {len(want)} frozen")
    sys.exit(1)
bad = 0
for name in got:
    a = np.asarray(Image.open(os.path.join(mine, name)).convert("RGB"))
    b = np.asarray(Image.open(os.path.join(frozen, name)).convert("RGB"))
    if not (a.shape == b.shape and np.array_equal(a, b)):
        print(f"  [DIFF] {name}"); bad += 1
print(f"  {len(got) - bad}/{len(got)} segments identical to the frozen set")
sys.exit(1 if bad else 0)
PY

  echo
  echo "--- ink coverage (this gate can fail; see check_coverage.py) ---"
  cp "$EX/Intermediate/segment_manifest.json" "$WORK/segs/segment_manifest.json"
  python3 "$HERE/tools/check_coverage.py" "$WORK/segs" --pages "$WORK/pages" || RC=1

  echo
  echo "--- figure crops vs the frozen figures ---"
  mkdir -p "$WORK/figs" && cp "$EX/Deliverable/figures/"*.png "$WORK/figs/"
  python3 "$HERE/tools/crop_figures.py" "$EX/Intermediate/figure_crops.json" \
      "$WORK/pages" "$WORK/figs" --extra-pages "600=$WORK/pages600" --check || RC=1

  echo
  if [ "${RC:-0}" = 0 ]; then
    echo "REPRODUCED: pages, segments and figures came back identical."
    echo "Stage 1 is intact on this machine. Run ./verify.sh (no flag) to"
    echo "measure the delivered PDF, or rebuild_example.sh to prove LaTeX."
  else
    echo "NOT REPRODUCED -- see the DIFF lines above. Check that pdftoppm is"
    echo "poppler's and that Worked_Example/ was not edited."
  fi
  exit "${RC:-0}"
fi

PDF=$(find_one \
  "$HERE/Worked_Example/Deliverable/hc6001_2024-10-22_scattering_hamiltonian.pdf" \
  "$HERE/../Final_Product_Ready/hc6001_2024-10-22_scattering_hamiltonian.pdf")
ALT=$(find_one \
  "$HERE/Worked_Example/Deliverable/alt_text.json" \
  "$HERE/../Final_Product_Ready/alt_text.json")
FIGS=$(find_one \
  "$HERE/Worked_Example/Deliverable/figures" \
  "$HERE/../Final_Product_Ready/figures")
HTML=$(find_one \
  "$HERE/Worked_Example/Deliverable/html/notes.html" \
  "$HERE/../Final_Product_Ready/html/notes.html")
TOOLS=$(find_one "$HERE/tools" "$HERE/../tools")
VERA="${1:-verapdf}"

[ -n "${PDF:-}" ] || { echo "FATAL: could not find the delivered PDF"; exit 2; }
echo "document : $PDF"
echo "md5      : $(python3 -c "import hashlib,sys; print(hashlib.md5(open(sys.argv[1],'rb').read()).hexdigest())" "$PDF")"
echo "tools    : $TOOLS"
echo
echo "Frozen reference md5 (16 August 2026): 85b05d31081368d8b811063456c7f769"
echo

echo "=============================================================="
echo " 1. Conformance check (the floor, not the evidence)"
echo "=============================================================="
if command -v "$VERA" >/dev/null 2>&1 || [ -x "$VERA" ]; then
  echo "--- PDF/UA-2 (the standard this document declares) ---"
  "$VERA" -f ua2 --format text "$PDF" | tail -3
  echo "--- PDF/UA-1 (run for contrast; disagreements are informative) ---"
  "$VERA" -f ua1 --format text "$PDF" | tail -3
  echo "Note: UA-1 failures on the file header and pdfuaid:part are expected"
  echo "of a PDF 2.0 / UA-2 document and are not defects. The clause 7.7"
  echo "failures are the known Formula /Alt gap described in the report."
else
  echo "veraPDF not found at '$VERA' -- conformance NOT checked."
  echo "Get it free from https://verapdf.org and re-run:  ./verify.sh /path/to/verapdf"
fi
echo

echo "=============================================================="
echo " 2. Step 4d structural acceptance tests (the actual evidence)"
echo "=============================================================="
python3 "$TOOLS/check_structure.py" "$PDF" ${ALT:+--alt "$ALT"} --sections 16
STRUCT=$?
echo

echo "=============================================================="
echo " 3. Contrast, measured rather than estimated"
echo "=============================================================="
[ -n "${FIGS:-}" ] && python3 "$TOOLS/check_contrast.py" --images "$FIGS"
python3 "$TOOLS/check_contrast.py" --pdf "$PDF"
echo

if [ -n "${HTML:-}" ]; then
  echo "=============================================================="
  echo " 4. HTML companion, held to the same WCAG 2.1 AA bar"
  echo "=============================================================="
  python3 - "$HTML" <<'PY'
import re, sys
h = open(sys.argv[1], encoding='utf-8').read()
imgs = re.findall(r'<img\b[^>]*>', h)
levels = sorted({int(x) for x in re.findall(r'<h(\d)\b', h)})
skips = [ (levels[i], levels[i+1]) for i in range(len(levels)-1)
          if levels[i+1] - levels[i] > 1 ]
checks = [
 ("MathML elements",        len(re.findall(r'<math\b', h)),            lambda v: v > 0),
 ("equations rasterised",   len(re.findall(r'<img[^>]*class="[^"]*math', h)), lambda v: v == 0),
 ("heading levels",         levels,                                    lambda v: v[:1] == [1]),
 ("skipped heading levels", skips,                                     lambda v: not v),
 ("images without alt",     sum('alt=' not in i for i in imgs),        lambda v: v == 0),
 ("alt=\"PIC\" left over",  sum('alt="PIC"' in i or "alt='PIC'" in i for i in imgs), lambda v: v == 0),
 ("data-table <th>",        len(re.findall(r'<th\b', h)),              lambda v: v > 0),
 ("table captions",         len(re.findall(r'<caption\b', h)),         lambda v: v > 0),
 ("real <ul>/<ol> lists",   len(re.findall(r'<[uo]l\b', h)),           lambda v: v > 0),
 ("html lang set",          bool(re.search(r'<html[^>]*\blang=', h)),  lambda v: v),
]
bad = 0
for name, val, ok in checks:
    good = ok(val)
    bad += not good
    print(f"  [{'PASS' if good else 'FAIL'}] {name:26s} {val}")
print(f"\n  {'HTML COMPANION OK' if not bad else f'HTML COMPANION: {bad} FAILED'}")
PY
  echo
fi

echo "=============================================================="
echo " Acceptance summary"
echo "=============================================================="
echo "The four numeric tests that gate this pipeline:"
echo "  1. headings 1:1 with the source outline"
echo "  2. ZERO text operators unreachable from the tag tree"
echo "  3. nothing meaningful marked as an artifact"
echo "  4. no figure clustered at the end of reading order"
echo
if [ "${STRUCT:-1}" -eq 0 ]; then
  echo "RESULT: all structural acceptance tests PASSED."
else
  echo "RESULT: at least one structural acceptance test FAILED (see section 2)."
fi
exit "${STRUCT:-1}"
