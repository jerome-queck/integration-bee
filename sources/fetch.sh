#!/usr/bin/env bash
# Fetch official UK University Integration Bee public materials.
# Extracts ALL rounds from Resource_pack.zip into:
#   sources/past/r1/YYYY/
#   sources/past/r2/YYYY/          (flat years)
#   sources/past/r2/2025/uk|sg/    (regional when both exist)
#   sources/past/r3/YYYY/
# Idempotent. Migrates legacy sources/past/YYYY -> r1/YYYY if present.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="https://integration.soc.srcf.net"
cd "$DIR"

fetch() {
  local url="$1" out="$2"
  echo "GET $url -> $out"
  curl -fL --retry 3 --retry-delay 1 -o "$out" "$url"
  [[ -s "$out" ]] || { echo "FAIL empty: $out"; exit 1; }
}

fetch "$BASE/" "index.html"
fetch "$BASE/pastcomp.html" "pastcomp.html"
fetch "$BASE/UK_University_Integration_Bee_Syllabus.pdf" "UK_University_Integration_Bee_Syllabus.pdf"
fetch "$BASE/UK_University_Integration_Bee_Techniques_Guide.pdf" "UK_University_Integration_Bee_Techniques_Guide.pdf"
fetch "$BASE/Integration_Competition_Sample_problems.pdf" "Integration_Competition_Sample_problems.pdf"
fetch "$BASE/Virtual_integration_competition_sample_hints.pdf" "Virtual_integration_competition_sample_hints.pdf"
fetch "$BASE/Integration_bee_sample_problems_answers.pdf" "Integration_bee_sample_problems_answers.pdf"
fetch "$BASE/UK%20University%20integration%20bee%20sample%20problems%20solutions.pdf" \
  "UK_University_integration_bee_sample_problems_solutions.pdf"
fetch "$BASE/Resource%20pack.zip" "Resource_pack.zip"

echo "Verifying sha256sums (files listed that exist)..."
if command -v sha256sum >/dev/null; then
  while read -r hash name; do
    [[ -z "${name:-}" || "$hash" =~ ^# ]] && continue
    if [[ -f "$name" ]]; then
      echo "$hash  $name" | sha256sum -c -
    else
      echo "SKIP (missing): $name"
    fi
  done < sha256sums
else
  echo "WARN: sha256sum not found; skipped checksum verify"
fi

# Migrate legacy past/YYYY -> past/r1/YYYY
if [[ -d past ]]; then
  for yd in past/[0-9][0-9][0-9][0-9]; do
    [[ -d "$yd" ]] || continue
    year="$(basename "$yd")"
    mkdir -p "past/r1/$year"
    for f in "$yd"/*; do
      [[ -f "$f" ]] || continue
      base="$(basename "$f")"
      if [[ ! -e "past/r1/$year/$base" ]]; then
        cp "$f" "past/r1/$year/$base"
        echo "migrate $yd/$base -> past/r1/$year/$base"
      fi
    done
    rm -rf "$yd"
    echo "removed legacy $yd"
  done
fi

python3 - <<'PY'
"""Extract Round 1/2/3 PDFs from Resource_pack.zip into sources/past/r{1,2,3}/."""
from __future__ import annotations
import re
import zipfile
from pathlib import Path

DIR = Path(".").resolve()
ZIP = DIR / "Resource_pack.zip"
PAST = DIR / "past"
PAST.mkdir(exist_ok=True)

def sanitize(name: str) -> str:
    return name.replace(" ", "_")

def classify(zip_path: str) -> Path | None:
    if not zip_path.startswith("Resource pack/"):
        return None
    rest = zip_path[len("Resource pack/") :]
    if not rest or rest.endswith("/"):
        return None
    if rest == "Resource pack 2025.zip":
        return None  # older nested subset; outer zip is authoritative
    m = re.match(r"^Round ([123])/(\d{4})/(.+)$", rest)
    if not m:
        return None
    rnd, year, tail = m.group(1), m.group(2), m.group(3)
    if rnd == "2" and year == "2025":
        if tail.startswith("SG version/"):
            return Path(f"r2/{year}/sg/{sanitize(Path(tail).name)}")
        if tail.startswith("UK Version/"):
            return Path(f"r2/{year}/uk/{sanitize(Path(tail).name)}")
        return Path(f"r2/{year}/{sanitize(Path(tail).name)}")
    if rnd == "3":
        return Path(f"r3/{year}/{sanitize(Path(tail).name)}")
    return Path(f"r{rnd}/{year}/{sanitize(Path(tail).name)}")

zf = zipfile.ZipFile(ZIP)
n = 0
for info in zf.infolist():
    if info.is_dir():
        continue
    if info.filename.endswith("Formula_sheet.pdf"):
        (DIR / "Formula_sheet.pdf").write_bytes(zf.read(info))
        print("OK Formula_sheet.pdf")
        continue
    dest_rel = classify(info.filename)
    if dest_rel is None:
        continue
    out = PAST / dest_rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(zf.read(info))
    n += 1
    print(f"OK past/{dest_rel.as_posix()}")
print(f"OK: extracted {n} round PDFs under past/r1|r2|r3/")
PY

echo "OK: sources fetched. All-rounds PDFs under past/r1|r2|r3/"
