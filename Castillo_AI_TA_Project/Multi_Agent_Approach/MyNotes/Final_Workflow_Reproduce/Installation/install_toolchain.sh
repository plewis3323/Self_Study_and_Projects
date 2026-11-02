#!/usr/bin/env bash
# Installs the toolchain needed to build a tagged, PDF/UA-targeting notes PDF.
#
# Accessibility features require a 2024-or-later LaTeX kernel. The TeX Live in
# Debian/Ubuntu repositories (2022) cannot tag mathematics at all: it accepts
# \DocumentMetadata, silently ignores the modules, and the untagged PDF still
# passes a conformance checker. That is why this script installs an upstream
# TeX Live next to the system one rather than using apt.
#
# Usage:
#   bash install_toolchain.sh [PREFIX]
#   PREFIX defaults to $HOME/texlive  (~1.2 GB, 15-30 min)
set -euo pipefail

PREFIX="${1:-$HOME/texlive}"
echo "Installing TeX Live into $PREFIX (about 1.2 GB) ..."

work=$(mktemp -d)
cd "$work"
curl -sLO https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar xzf install-tl-unx.tar.gz
cd install-tl-*

year=$(date +%Y)
cat > tl.profile <<PROFILE
selected_scheme scheme-medium
TEXDIR $PREFIX/$year
TEXMFLOCAL $PREFIX/texmf-local
TEXMFSYSCONFIG $PREFIX/$year/texmf-config
TEXMFSYSVAR $PREFIX/$year/texmf-var
instopt_adjustpath 0
tlpdbopt_install_docfiles 0
tlpdbopt_install_srcfiles 0
PROFILE

./install-tl -profile tl.profile -no-interaction

BIN="$PREFIX/$year/bin/x86_64-linux"
if [ ! -d "$BIN" ]; then
  BIN=$(echo "$PREFIX/$year/bin/"*)
fi
export PATH="$BIN:$PATH"

# packages this pipeline needs beyond scheme-medium
tlmgr install \
  cancel fancybox ulem booktabs enumitem mathtools hyperxmp was \
  float accsupp caption bookmark tex4ht make4ht unicode-math \
  luatex85 biber

echo
echo "Done. Add this to your shell profile:"
echo "    export PATH=$BIN:\$PATH"
echo
echo "Then:"
echo "    pip install -r requirements.txt"
echo "    sudo apt install poppler-utils   # pdftoppm, the reference renderer:"
echo "    #   every seam row and crop box in this pipeline is a pixel"
echo "    #   coordinate in a pdftoppm raster, and other rasterisers do not"
echo "    #   agree with it -- not even on the page height."
echo "    # veraPDF (conformance checker): https://verapdf.org"
echo
echo "Probe the install before any real run:"
echo "    lualatex probe.tex && lualatex probe.tex && lualatex probe.tex"
echo "and inspect probe.pdf for /Formula /L /Table /TH /Alt."
echo "If any is missing, the kernel is still too old — do not start the pipeline."
