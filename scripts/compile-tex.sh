#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
shopt -s nullglob
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
