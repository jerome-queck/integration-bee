#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
shopt -s nullglob

compile_sample() {
  local texinputs="$1"
  local dir status
  dir="$(mktemp -d)"
  status=0
  (
    cd "$dir"
    if [[ -n "$texinputs" ]]; then
      export TEXINPUTS="$texinputs"
    else
      unset TEXINPUTS
    fi
    latexmk -r "$ROOT/templates/latexmkrc" -pdf -interaction=nonstopmode \
      "$ROOT/units/01-foundations-substitution/teaching.tex"
  ) || status=$?
  rm -rf "$dir"
  return "$status"
}

if ! compile_sample ""; then
  echo "FAIL unit sample did not compile outside the repo root. templates/latexmkrc must put its own directory on TEXINPUTS." >&2
  exit 1
fi
if ! compile_sample "/no/such/tex/tree"; then
  echo "FAIL unit sample lost article.cls because TEXINPUTS was already set. templates/latexmkrc must keep an empty TEXINPUTS component." >&2
  exit 1
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
