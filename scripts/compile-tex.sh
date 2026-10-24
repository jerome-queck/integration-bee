#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
shopt -s nullglob

sample_dir="$(mktemp -d)"
sample_status=0
(
  cd "$sample_dir"
  latexmk -r "$ROOT/templates/latexmkrc" -pdf -interaction=nonstopmode \
    "$ROOT/units/01-foundations-substitution/teaching.tex"
) || sample_status=$?
rm -rf "$sample_dir"
if [[ "$sample_status" -ne 0 ]]; then
  echo "FAIL unit sample did not compile outside the repo root. templates/latexmkrc must put its own directory on TEXINPUTS." >&2
  exit "$sample_status"
fi
echo "PASS latex sample"

files=(units/*/*.tex templates/round1-sim.tex)
for f in "${files[@]}"; do
  echo "LATEX $f"
  latexmk -r templates/latexmkrc -pdf -interaction=nonstopmode "$f"
done
for f in "${files[@]}"; do
  latexmk -r templates/latexmkrc -C "$f" >/dev/null
done
rm -rf .latex-aux .latex-out
echo "PASS latex (${#files[@]} files)"
