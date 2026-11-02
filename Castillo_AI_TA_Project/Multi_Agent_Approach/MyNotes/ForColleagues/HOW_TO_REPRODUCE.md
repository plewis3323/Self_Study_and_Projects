# Not the process

The process is: open this folder in an agent platform and send
`Multi_Agent_Outline.md`. See `README.md`. Everything on this page is optional
and none of it replaces feeding the markdown.

## Checking the kit before you trust it

| Command | What it establishes | Needs |
|---|---|---|
| `./verify.sh --reproduce` | Stage 1 is deterministic and intact here — the source PDF re-renders, re-segments and re-crops to artifacts pixel-identical to the frozen ones. Run this first; it is the cheapest proof that the kit and your toolchain agree. | python3, poppler |
| `./verify.sh /path/to/verapdf` | The delivered PDF measures what the report says — conformance plus the four Step 4d numeric tests, contrast, and the HTML companion. | + veraPDF |
| `bash rebuild_example.sh [--html]` | Your LuaLaTeX produces a tagged document with the same structure as the frozen one. Byte-identical output is *not* expected; identical structure counts are. | + TeX Live 2024+ |

`rebuild_example.sh` recompiles an already-transcribed `.tex`. It does not
segment, review, or transcribe anything — it is a toolchain proof, not a run.

## Installing what those need

```bash
bash install_toolchain.sh          # TeX Live 2024+, ~1.2 GB, 15-30 min
export PATH=$HOME/texlive/2026/bin/x86_64-linux:$PATH
pip install -r requirements.txt    # pymupdf, pillow, numpy
sudo apt install poppler-utils     # pdftoppm -- the reference page renderer
# veraPDF (conformance checker), free: https://verapdf.org
```

Two of these are not interchangeable with their obvious alternatives:

- **TeX Live must be 2024 or later.** The version in the Debian/Ubuntu
  repositories accepts `\DocumentMetadata`, ignores the tagging modules, and
  emits an untagged PDF that still passes a conformance checker. That silent
  pass is why `install_toolchain.sh` installs upstream TeX Live beside the
  system one instead of using `apt`. Probe before running anything real:
  `lualatex probe.tex` three times, then look in `probe.pdf` for `/Formula`,
  `/L`, `/Table`, `/TH` and `/Alt`.
- **`pdftoppm`, not another rasteriser.** Seam rows and figure crop boxes are
  pixel coordinates in one particular raster. Poppler and PyMuPDF disagree on
  antialiasing and, on US Letter at 300 dpi, on the page height itself (3301
  rows against 3300). `render_pages.py` falls back to PyMuPDF and records that
  it did, but boxes measured under one engine do not transfer to the other.

## Agent platforms

Cursor Agent, Claude Code, Codex CLI — anything that can run commands, write
files and see images **on the machine holding this folder**. A browser chat
window cannot run this. Reviewers are independent subagents; if your tool
cannot spawn them, the Prime Agent stops at each review gate and says so, and
you run the reviewers as separate conversations.
