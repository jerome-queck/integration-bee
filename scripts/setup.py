#!/usr/bin/env python3
"""One-step, idempotent setup for the Integration Bee pack.

Works on macOS, Linux, and Windows with the standard library only:

    python3 scripts/setup.py          # macOS / Linux
    py scripts\\setup.py               # Windows

It creates `.venv/` in the repo root, installs the pinned packages from
`requirements.txt`, and runs a smoke check (imports plus `doctor`).
Running it again only re-installs when `requirements.txt` changed.
Prints `SETUP OK` and exits 0 on success.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / ".venv"
REQS = ROOT / "requirements.txt"
STAMP = VENV / ".requirements.sha256"
MIN_PY = (3, 11)


def venv_python() -> Path:
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def ensure_venv() -> Path:
    py = venv_python()
    if py.exists():
        print(f"ok   .venv exists ({py.relative_to(ROOT)})")
    else:
        print("make .venv")
        venv.EnvBuilder(with_pip=True, clear=False).create(VENV)
    return py


def ensure_packages(py: Path) -> None:
    digest = hashlib.sha256(REQS.read_bytes()).hexdigest()
    if STAMP.exists() and STAMP.read_text().strip() == digest:
        print("ok   pinned packages already installed")
        return
    run([str(py), "-m", "pip", "install", "--disable-pip-version-check", "-q", "-r", str(REQS)])
    STAMP.write_text(digest + "\n")


def smoke(py: Path) -> None:
    run([str(py), "-c", "import sympy, yaml, mpmath; print('sympy', sympy.__version__)"])
    run([str(py), str(ROOT / "scripts" / "control-integration-bee"), "doctor"])


def main() -> int:
    if sys.version_info < MIN_PY:
        print(f"FAIL need Python {MIN_PY[0]}.{MIN_PY[1]}+; this is {sys.version.split()[0]}")
        return 1
    try:
        py = ensure_venv()
        ensure_packages(py)
        smoke(py)
    except subprocess.CalledProcessError as exc:
        print(f"FAIL setup step exited {exc.returncode}: {' '.join(map(str, exc.cmd))}")
        return 1
    print("SETUP OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
