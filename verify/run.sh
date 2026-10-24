#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
if [[ ! -x "$PY" ]]; then PY="python3"; fi
fail=0

echo "== sources presence =="
need=(
  "$ROOT/syllabus-map.md"
  "$ROOT/STATE.md"
  "$ROOT/sources/sha256sums"
  "$ROOT/sources/fetch.sh"
  "$ROOT/sources/UK_University_Integration_Bee_Syllabus.pdf"
  "$ROOT/sources/UK_University_Integration_Bee_Techniques_Guide.pdf"
  "$ROOT/sources/Integration_Competition_Sample_problems.pdf"
  "$ROOT/sources/Virtual_integration_competition_sample_hints.pdf"
  "$ROOT/sources/Integration_bee_sample_problems_answers.pdf"
  "$ROOT/sources/UK_University_integration_bee_sample_problems_solutions.pdf"
  "$ROOT/sources/Formula_sheet.pdf"
  "$ROOT/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf"
  "$ROOT/sources/user/yang-topics-inventory.md"
  "$ROOT/units/01-foundations-substitution/meta.yaml"
  "$ROOT/units/01-foundations-substitution/teaching.tex"
  "$ROOT/units/01-foundations-substitution/drills.tex"
  "$ROOT/units/01-foundations-substitution/solutions.tex"
  "$ROOT/units/01-foundations-substitution/drills.md"
  "$ROOT/verify/drills_unit1.json"
)
for f in "${need[@]}"; do
  if [[ ! -e "$f" ]]; then echo "FAIL missing: $f"; fail=1; else echo "OK $f"; fi
done

echo "== concept unit shape =="
shopt -s nullglob
for udir in "$ROOT"/units/[0-9][0-9]-*/; do
  base="$(basename "$udir")"
  n="${base%%-*}"
  n=$((10#$n))
  for f in meta.yaml teaching.tex drills.tex solutions.tex drills.md; do
    if [[ ! -e "$udir$f" ]]; then echo "FAIL missing: $udir$f"; fail=1; else echo "OK $udir$f"; fi
  done
  dj="$ROOT/verify/drills_unit${n}.json"
  if [[ ! -e "$dj" ]]; then echo "FAIL missing: $dj"; fail=1; else echo "OK $dj"; fi
done
shopt -u nullglob

echo "== yang 1.1–1.20 in syllabus-map =="
for i in $(seq 1 20); do
  if grep -q "yang:1\.$i" "$ROOT/syllabus-map.md"; then
    echo "OK yang:1.$i"
  else
    echo "FAIL syllabus-map missing yang:1.$i"; fail=1
  fi
done

echo "== unit_order_check =="
"$PY" "$ROOT/verify/unit_order_check.py" || fail=1

echo "== check_math (all drills_unit*.json) =="
"$PY" "$ROOT/verify/check_math.py" || fail=1

echo "== mutation: wrong answer must fail =="
if "$PY" "$ROOT/verify/check_math.py" --mutate-wrong; then
  echo "FAIL mutation: expected non-zero exit"; fail=1
else
  echo "PASS mutation (wrong answer rejected)"
fi

echo "== past_presence_check =="
"$PY" "$ROOT/verify/past_presence_check.py" || fail=1

echo "== check_samples (sympy-safe official sample answers) =="
"$PY" "$ROOT/verify/check_samples.py" || fail=1

echo "== generate_practice seed yang smoke =="
"$PY" "$ROOT/verify/generate_practice.py" --tag yang:1.1 --tag yang:1.5 --tag yang:1.18 --tag yang:1.19 >/tmp/ibe_practice.out || fail=1
wc -l /tmp/ibe_practice.out

echo "== all_rounds_check (Resource pack r1|r2|r3) =="
"$PY" "$ROOT/verify/all_rounds_check.py" || fail=1

echo "== problem catalog =="
"$PY" "$ROOT/verify/catalog_check.py" || fail=1
"$PY" "$ROOT/verify/catalog_check.py" --expect-fail invented-sympy || fail=1
"$PY" "$ROOT/verify/catalog_check.py" --expect-fail missing-cite || fail=1
"$PY" "$ROOT/verify/catalog_check.py" --expect-fail yang-invented || fail=1
"$PY" "$ROOT/verify/catalog_check.py" --expect-fail dropped-record || fail=1

echo "== turn contract =="
"$PY" "$ROOT/verify/turn_contract_check.py" || fail=1

if [[ "$fail" -ne 0 ]]; then echo "FAIL integration-bee verify"; exit 1; fi
echo "PASS integration-bee verify (multi-unit gates)"
