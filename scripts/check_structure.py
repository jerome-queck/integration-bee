#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

import yaml

from generate_agents_md import ENFORCERS, ROOT

fail = 0
for _rule, rel in ENFORCERS:
    if not (ROOT / rel).exists():
        print(f"FAIL missing enforcer {rel}")
        fail = 1

def ignored(path: str) -> bool:
    proc = subprocess.run(
        ["git", "check-ignore", "-q", "--no-index", path],
        cwd=ROOT,
    )
    return proc.returncode == 0

if not ignored("trackers/live/attempts.json"):
    print("FAIL trackers/live/attempts.json is not ignored")
    fail = 1
if not ignored("trackers/live/submissions/default/photo.png"):
    print("FAIL submission photo is not ignored")
    fail = 1
problems = "sources/past/r1/2020/2020_Integration_Competition_Problems.pdf"
if ignored(problems):
    print(f"FAIL {problems} is ignored")
    fail = 1
if not (ROOT / problems).is_file():
    print(f"FAIL {problems} missing from the tree")
    fail = 1
syllabus = "sources/UK_University_Integration_Bee_Syllabus.pdf"
if ignored(syllabus):
    print(f"FAIL {syllabus} is ignored")
    fail = 1
if not (ROOT / syllabus).is_file():
    print(f"FAIL {syllabus} missing from the tree")
    fail = 1
if not ignored("sources/Resource_pack.zip"):
    print("FAIL sources/Resource_pack.zip is not ignored")
    fail = 1
if not ignored("progress.local.json"):
    print("FAIL progress.local.json is not ignored")
    fail = 1
yang = "sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf"
if ignored(yang):
    print("FAIL Yang PDF is ignored")
    fail = 1
if not (ROOT / yang).is_file():
    print("FAIL Yang PDF missing from the tree")
    fail = 1

for path in sorted((ROOT / "units").glob("[0-9][0-9]-*/meta.yaml")):
    rel = path.relative_to(ROOT)
    try:
        doc = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        print(f"FAIL {rel} did not parse: {exc}")
        fail = 1
        continue
    if not isinstance(doc, dict) or not isinstance(doc.get("title"), str) or not doc["title"].strip():
        print(f"FAIL {rel} needs a title")
        fail = 1

skill = ROOT / ".cursor/skills/formal-verify-integration-bee/SKILL.md"
text = skill.read_text()
marker = "last_confirmed: "
line = next((ln for ln in text.splitlines() if ln.startswith(marker)), "")
recorded = line[len(marker):].strip()
blob = subprocess.run(
    ["git", "rev-parse", "HEAD:verify/model.py"],
    cwd=ROOT,
    capture_output=True,
    text=True,
)
blob_id = blob.stdout.strip()
if blob.returncode != 0 or not blob_id:
    print("FAIL formal sync could not read verify/model.py")
    fail = 1
elif recorded != blob_id:
    print(f"FAIL formal sync {recorded} != {blob_id}")
    fail = 1

if fail:
    sys.exit(1)
print("PASS structure")
