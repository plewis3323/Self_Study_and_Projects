# Feed `Multi_Agent_Outline.md` to an agent. That is the process.

1. Unzip this kit and open the folder in an **agent platform that can run
   commands, write files, and see images on this machine** — Cursor Agent,
   Claude Code, or Codex CLI. A browser chat window cannot run this.
2. Put **one handwritten / board PDF per lecture** into `input/`.
3. Attach or open **`Multi_Agent_Outline.md`** and send it to the agent.
   That file is the kickoff and the specification. Do not paste a second
   prompt. The agent probes the toolchain, then runs Stages 0–5 until the
   review loops close.

First time on a machine: if the agent reports LuaLaTeX missing, let it run
`bash install_toolchain.sh` (~1.2 GB) and `pip install -r requirements.txt`.
Also install poppler (`apt install poppler-utils`) — `pdftoppm` is the
renderer every pixel coordinate in the pipeline is measured against.

`Worked_Example/` is a completed run of this same markdown on the 22 October
2024 HC 6001 lecture, so you can see what “done” looks like. Do not write a
new lecture into that folder. It is frozen at the state it was audited in;
`CHANGES_SINCE_RUN.md` lists what has changed in the tooling since, so a
number in its run log that no longer matches a tool reads as history rather
than as a contradiction.

Optional, not the process:

| Command | Proves |
|---|---|
| `./verify.sh --reproduce` | The pipeline still works here: re-renders, re-segments and re-crops the example from its source PDF and demands the results come back pixel-identical. No LaTeX needed — about a minute. |
| `./verify.sh [path/to/verapdf]` | The delivered PDF still measures what the report claims — conformance plus all four Step 4d numeric tests. |
| `bash rebuild_example.sh [--html]` | Your LuaLaTeX can compile the already-transcribed example. Not a pipeline run: it re-segments nothing and reviews nothing. |
| `md5sum -c CHECKSUMS.txt` | The 95 files arrived intact. |
