#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from generate_agents_md import ENFORCERS, ROOT

fail = 0
for _rule, rel in ENFORCERS:
    if not (ROOT / rel).exists():
        print(f"FAIL missing enforcer {rel}")
        fail = 1

def ignored(path: str) -> bool:
    proc = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT)
    return proc.returncode == 0

if not ignored("trackers/live/attempts.json"):
    print("FAIL trackers/live/attempts.json is not ignored")
    fail = 1
if not ignored("sources/past/r1/2020/example.pdf"):
    print("FAIL sources/past pdf is not ignored")
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

skill = ROOT / ".cursor/skills/formal-verify-integration-bee/SKILL.md"
text = skill.read_text()
marker = "last_confirmed: "
line = next((ln for ln in text.splitlines() if ln.startswith(marker)), "")
recorded = line[len(marker):].strip()
last = subprocess.run(
    ["git", "log", "-1", "--format=%H", "--", "verify/model.py"],
    cwd=ROOT,
    capture_output=True,
    text=True,
).stdout.strip()
if last and recorded != last:
    print(f"FAIL formal sync {recorded} != {last}")
    fail = 1

if fail:
    sys.exit(1)
print("PASS structure")
