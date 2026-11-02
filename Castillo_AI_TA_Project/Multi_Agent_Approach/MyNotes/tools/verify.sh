#!/usr/bin/env bash
# Re-run every acceptance check on the delivered document and print the numbers.
#
# Nothing here trusts a stored report: the conformance checker and all four
# Step 4d numeric tests are executed against the PDF you have in front of you.
# A conformance pass alone is a floor, not evidence -- in the reference run a
# checker passed cleanly three times while 16 headings were mis-tagged and 24
# content operators sat outside the tag tree. The numeric tests are what
# caught those, so they are the acceptance criteria here.
#
#   ./verify.sh [path/to/verapdf]
#
# Requires: python3 with pymupdf, numpy, pillow. veraPDF is optional but
# strongly recommended; its absence is reported rather than skipped silently.

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

find_one() {                      # locate a file whether run from the package
  for p in "$@"; do [ -e "$p" ] && { echo "$p"; return; }; done
}

PDF=$(find_one \
  "$HERE/../01_Deliverable/hc6001_2024-10-22_scattering_hamiltonian.pdf" \
  "$HERE/../Final_Product_Ready/hc6001_2024-10-22_scattering_hamiltonian.pdf" \
  "$HERE/Final_Product_Ready/hc6001_2024-10-22_scattering_hamiltonian.pdf")
ALT=$(find_one "$HERE/../01_Deliverable/alt_text.json" \
  "$HERE/../Final_Product_Ready/alt_text.json" \
  "$HERE/Final_Product_Ready/alt_text.json")
FIGS=$(find_one "$HERE/../01_Deliverable/figures" \
  "$HERE/../Final_Product_Ready/figures" \
  "$HERE/Final_Product_Ready/figures")
HTML=$(find_one "$HERE/../01_Deliverable/html/notes.html" \
  "$HERE/../Final_Product_Ready/html/notes.html")
TOOLS=$(find_one "$HERE/../04_Reproduce/tools" "$HERE/../tools" "$HERE")
VERA="${1:-verapdf}"

[ -n "${PDF:-}" ] || { echo "FATAL: could not find the delivered PDF"; exit 2; }
echo "document : $PDF"
echo "tools    : $TOOLS"
echo

echo "=============================================================="
echo " 1. Conformance check (the floor, not the evidence)"
echo "=============================================================="
if command -v "$VERA" >/dev/null 2>&1 || [ -x "$VERA" ]; then
  echo "--- PDF/UA-1 (the standard this document declares, and the one PAC 2026 checks) ---"
  "$VERA" -f ua1 --format text "$PDF" | tail -3
  echo "--- PDF/UA-2 (run for contrast; disagreements are informative) ---"
  "$VERA" -f ua2 --format text "$PDF" | tail -3
  echo "Note: 2026-08-20 this document switched from declaring UA-2 to declaring"
  echo "UA-1, specifically because PAC 2026 (the institutional checker) tests"
  echo "against UA-1, and UA-2's /AF-only math tagging left 189/198 formulas"
  echo "with no alt text PAC would recognize. UA-2 now fails here on pdfversion"
  echo "alone (this file is PDF 1.7) -- expected, not a defect."
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
from collections import Counter
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
