#!/usr/bin/env bash
# Rebuild the worked-example tagged PDF from the already-transcribed source.
# Optional toolchain proof — not a pipeline run. It does not
# re-segment or re-review.
#
#   bash rebuild_example.sh [--html]
#
# Writes Worked_Example/Rebuild/. Does not overwrite the frozen Deliverable.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
EX="$HERE/Worked_Example"
SRC="$EX/Intermediate/notes_src.tex"
ALT="$EX/Deliverable/alt_text.json"
STY="$HERE/style/goldsteinnotes.sty"
OUT="$EX/Rebuild"
HTML_FLAG="${1:-}"

command -v lualatex >/dev/null || {
  echo "FATAL: lualatex not on PATH. Run install_toolchain.sh and export PATH."
  exit 2
}

mkdir -p "$OUT/figures"
cp -f "$STY" "$OUT/goldsteinnotes.sty"
cp -f "$EX/Deliverable/figures/"*.png "$OUT/figures/"
cp -f "$EX/Deliverable/figures/figure_crops.json" "$OUT/figures/" 2>/dev/null || true

python3 "$HERE/tools/make_accessible.py" \
  "$SRC" \
  "$OUT/hc6001_2024-10-22_scattering_hamiltonian.tex" \
  "$ALT" \
  --title "Scattering by a Central Potential; the Hamiltonian" \
  --author "HC 6001 -- Dr. Castillo" \
  --modern

# LuaLaTeX exits non-zero on *recovered* errors under -interaction=nonstopmode,
# and it still writes a complete PDF when it does. Under `set -e` that killed
# this script after the third pass, before it printed the md5 or ran a single
# structural test -- a rebuild that in fact succeeded looked like a silent
# failure. Do not drop `set -e`: keep it, and account for the exit status here.
# Recovered errors are then reported as a number rather than swallowed, because
# they are a real signal (a preamble macro misfiring, for instance) even when
# the PDF is fine.
BUILD_LOG="$OUT/build.log"
: > "$BUILD_LOG"
for pass in 1 2 3; do
  echo "LuaLaTeX pass $pass/3 ..."
  ( cd "$OUT" && lualatex -interaction=nonstopmode \
      hc6001_2024-10-22_scattering_hamiltonian.tex ) >> "$BUILD_LOG" 2>&1 \
    && rc=0 || rc=$?
  [ "$pass" = 3 ] && LAST_RC=$rc
done

PDF="$OUT/hc6001_2024-10-22_scattering_hamiltonian.pdf"
if [ ! -f "$PDF" ]; then
  echo "FATAL: no PDF produced. Last 40 lines of $BUILD_LOG:"
  tail -40 "$BUILD_LOG"
  exit 2
fi

RECOVERED=$(grep -c '^! ' "$BUILD_LOG" || true)
echo
echo "lualatex exit status : ${LAST_RC:-0}   recovered TeX errors: $RECOVERED"
if [ "$RECOVERED" -gt 0 ]; then
  echo "  (a non-zero count is not cosmetic -- inspect $BUILD_LOG. The PDF"
  echo "   below was still written; check its structure before trusting it.)"
  grep '^! ' "$BUILD_LOG" | sort | uniq -c | sort -rn | head -5 | sed 's/^/  /'
fi
echo
echo "rebuilt : $PDF"
echo "md5     : $(python3 -c "import hashlib,sys; print(hashlib.md5(open(sys.argv[1],'rb').read()).hexdigest())" "$PDF")"
echo "frozen  : 85b05d31081368d8b811063456c7f769  (bytes will differ; structure should not)"
echo
python3 "$HERE/tools/check_structure.py" "$PDF" --alt "$ALT" --sections 16

if [ "$HTML_FLAG" = "--html" ]; then
  echo
  echo "Building HTML companion (make4ht)..."
  OUT="$OUT" python3 - <<'PY'
from pathlib import Path
import os
out = Path(os.environ["OUT"])
src = (out / "hc6001_2024-10-22_scattering_hamiltonian.tex").read_text()
lines = src.splitlines(True)
body = []
i = 0
while i < len(lines):
    L = lines[i]
    if L.startswith("\\DocumentMetadata"):
        while i < len(lines) and not lines[i].strip().endswith("}"):
            i += 1
        i += 1
        continue
    if L.startswith("\\def\\GNmoderntagging") or L.startswith("\\usepackage{unicode-math}") \
       or L.startswith("\\setmathfont"):
        i += 1
        continue
    body.append(L)
    i += 1
(out / "notes.tex").write_text("".join(body))
PY
  (
    cd "$OUT"
    make4ht -u notes "mathml"
  )
  python3 "$HERE/tools/fix_html_alt.py" "$OUT/notes.html" "$ALT"
  python3 "$HERE/tools/fix_html_structure.py" "$OUT/notes.html"
  echo "HTML: $OUT/notes.html"
else
  echo
  echo "HTML skipped. Re-run with --html to build the companion."
fi
