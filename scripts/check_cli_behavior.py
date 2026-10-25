#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = [sys.executable, str(ROOT / "scripts" / "control-integration-bee")]


def run(args: list[str], data: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["IB_DATA_DIR"] = str(data)
    return subprocess.run(
        [*CLI, *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def detail(proc: subprocess.CompletedProcess[str]) -> str:
    return f"exit={proc.returncode}\nstdout:\n{proc.stdout[-600:]}\nstderr:\n{proc.stderr[-600:]}"


def body(proc: subprocess.CompletedProcess[str]):
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def turn(data: Path, payload: dict) -> subprocess.CompletedProcess[str]:
    path = data / "turn.json"
    path.write_text(json.dumps(payload))
    return run(["turn", "apply", "--file", str(path), "--format", "json"], data)


def main() -> int:
    fails: list[str] = []

    def check(cond: bool, label: str, extra: str = "") -> None:
        if cond:
            print(f"PASS {label}")
            return
        fails.append(label)
        print(f"FAIL {label}")
        if extra:
            print(extra)

    with tempfile.TemporaryDirectory(prefix="ib-cli-") as tmp:
        data = Path(tmp)
        doctor = run(["doctor", "--data-dir", "/tmp/not-the-doctor-label"], data)
        check(doctor.returncode == 0 and "READY integration-bee" in doctor.stdout, "doctor ready", detail(doctor))
        check(f"data_dir={data}" in doctor.stdout and "/tmp/not-the-doctor-label" not in doctor.stdout, "doctor ignores --data-dir", detail(doctor))

        help_out = run(["--help"], data)
        check(help_out.returncode == 0 and "List drills without answers." in help_out.stdout, "help names practice list", detail(help_out))
        check("Print one problem prompt." in help_out.stdout, "help names problems select", detail(help_out))
        bare = run(["practice"], data)
        joined = bare.stdout + bare.stderr
        check(bare.returncode == 2 and "{list,next,check}" in joined, "practice with no command names its commands", detail(bare))

        listed = run(["problems", "list", "--round", "R1", "--format", "json"], data)
        listed_doc = body(listed)
        check(
            listed.returncode == 0 and isinstance(listed_doc, dict) and listed_doc.get("count") == 280,
            "round R1 lists 280",
            detail(listed),
        )
        check(listed_doc is not None and "R1-2024-Q01" in listed.stdout and "answer_plain" not in listed.stdout, "round list hides answers", detail(listed))
        source = run(["problems", "list", "--source", "Resource_Pack", "--round", "r1", "--format", "json"], data)
        check(source.returncode == 0 and "unknown source" not in source.stderr, "source case folds", detail(source))
        page = run(["problems", "list", "--round", "r1", "--limit", "2", "--format", "json"], data)
        page_doc = body(page)
        check(
            page.returncode == 0
            and isinstance(page_doc, dict)
            and page_doc.get("count") == 280
            and len(page_doc.get("problems") or []) == 2,
            "limit keeps the match count and shortens the page",
            detail(page),
        )
        text = run(["problems", "list", "--round", "r1"], data)
        check(
            text.returncode == 0
            and "count=280" in text.stdout
            and "R1-2020-Q01" in text.stdout
            and "answer_plain" not in text.stdout
            and "answer_sympy" not in text.stdout
            and len(text.stdout) < len(listed.stdout),
            "text list is a table without answers",
            detail(text),
        )
        practice_text = run(["practice", "list", "--unit", "1"], data)
        check(
            practice_text.returncode == 0
            and practice_text.stdout.startswith("count=8\n")
            and "U01-D01" in practice_text.stdout
            and "U01-D08" in practice_text.stdout
            and '"drills"' not in practice_text.stdout
            and "answer_display" not in practice_text.stdout
            and r"\pi/4" not in practice_text.stdout,
            "practice text list hides the answer",
            detail(practice_text),
        )
        negative = run(["practice", "list", "--unit", "1", "--limit", "-1", "--format", "json"], data)
        check(negative.returncode == 2 and "limit must be >= 0" in negative.stderr and "Traceback" not in negative.stderr, "negative limit is refused", detail(negative))
        ambiguous = run(["problems", "select", "--round", "r1", "--format", "json"], data)
        check(
            ambiguous.returncode == 2 and "matched" in ambiguous.stderr and "R1-2020-Q01" in ambiguous.stderr,
            "ambiguous select names ids",
            detail(ambiguous),
        )

        fresh = run(["practice", "next", "--format", "json"], data)
        fresh_doc = body(fresh)
        check(
            fresh.returncode == 0
            and isinstance(fresh_doc, dict)
            and fresh_doc.get("id") == "U01-D01"
            and fresh_doc.get("reason") == "new"
            and "answer_display" not in fresh.stdout,
            "fresh next is U01-D01",
            detail(fresh),
        )

    with tempfile.TemporaryDirectory(prefix="ib-cli-grade-") as tmp:
        data = Path(tmp)
        plus_c = run(["practice", "check", "--id", "U01-D06", "--answer", "log(Abs(x**2+3*x+2))+C", "--format", "json"], data)
        plus_doc = body(plus_c)
        check(
            plus_c.returncode == 0 and isinstance(plus_doc, dict) and plus_doc.get("correct") is True,
            "indefinite +C matches",
            detail(plus_c),
        )
        plus_5 = run(["practice", "check", "--id", "U01-D06", "--answer", "log(Abs(x**2+3*x+2))+5", "--format", "json"], data)
        plus_5_doc = body(plus_5)
        check(
            plus_5.returncode == 0 and isinstance(plus_5_doc, dict) and plus_5_doc.get("correct") is True,
            "indefinite constant matches",
            detail(plus_5),
        )

    with tempfile.TemporaryDirectory(prefix="ib-cli-def-") as tmp:
        data = Path(tmp)
        shifted = run(["practice", "check", "--id", "U01-D08", "--answer", "pi/4+1", "--format", "json"], data)
        shifted_doc = body(shifted)
        check(
            shifted.returncode == 1 and isinstance(shifted_doc, dict) and shifted_doc.get("correct") is False,
            "definite constant is wrong",
            detail(shifted),
        )
        atan = run(["practice", "check", "--id", "U01-D08", "--answer", "atan(1)", "--format", "json"], data)
        atan_doc = body(atan)
        check(atan.returncode == 0 and isinstance(atan_doc, dict) and atan_doc.get("correct") is True, "atan(1) matches pi/4", detail(atan))

    with tempfile.TemporaryDirectory(prefix="ib-cli-parse-") as tmp:
        data = Path(tmp)
        junk = run(["practice", "check", "--id", "U01-D08", "--answer", "?", "--format", "json"], data)
        check(
            junk.returncode == 2
            and junk.stdout == ""
            and "answer did not parse:" in junk.stderr
            and not (data / "attempts.json").exists(),
            "unparsed answer writes nothing",
            detail(junk),
        )

    with tempfile.TemporaryDirectory(prefix="ib-cli-next-") as tmp:
        data = Path(tmp)
        solved = run(["practice", "check", "--id", "U01-D01", "--answer", "log(2)", "--format", "json"], data)
        check(solved.returncode == 0, "U01-D01 log(2)", detail(solved))
        nxt = run(["practice", "next", "--format", "json"], data)
        nxt_doc = body(nxt)
        check(
            nxt.returncode == 0 and isinstance(nxt_doc, dict) and nxt_doc.get("id") == "U01-D02" and nxt_doc.get("reason") == "new",
            "a correct drill is not served again the same day",
            detail(nxt),
        )

    with tempfile.TemporaryDirectory(prefix="ib-cli-due-") as tmp:
        data = Path(tmp)
        solved = run(["practice", "check", "--id", "U01-D08", "--answer", "pi/4", "--format", "json"], data)
        check(solved.returncode == 0, "U01-D08 stored", detail(solved))
        path = data / "attempts.json"
        stored = json.loads(path.read_text())
        stored["items"][0]["next_due"] = "2000-01-01"
        path.write_text(json.dumps(stored))
        due = run(["practice", "next", "--format", "json"], data)
        due_doc = body(due)
        check(
            due.returncode == 0 and isinstance(due_doc, dict) and due_doc.get("id") == "U01-D08" and due_doc.get("reason") == "due",
            "a due drill wins over a new one",
            detail(due),
        )

    answers = {
        "U01-D01": "log(2)",
        "U01-D02": "1/2",
        "U01-D03": "(exp(1)-1)/2",
        "U01-D04": "log(3)/2",
        "U01-D05": "1/3",
        "U01-D06": "log(x**2+3*x+2)",
        "U01-D07": "0",
        "U01-D08": "pi/4",
    }
    with tempfile.TemporaryDirectory(prefix="ib-cli-unit-") as tmp:
        data = Path(tmp)
        for drill_id, answer in answers.items():
            proc = run(["practice", "check", "--id", drill_id, "--answer", answer, "--format", "json"], data)
            got = body(proc)
            check(proc.returncode == 0 and isinstance(got, dict) and got.get("correct") is True, f"{drill_id} correct", detail(proc))
        nxt = run(["practice", "next", "--format", "json"], data)
        nxt_doc = body(nxt)
        check(
            nxt.returncode == 0 and isinstance(nxt_doc, dict) and nxt_doc.get("id") == "U02-D01",
            "the next unit drill follows a cleared unit",
            detail(nxt),
        )

    with tempfile.TemporaryDirectory(prefix="ib-cli-queue-") as tmp:
        data = Path(tmp)
        catalog = json.loads((ROOT / "trackers" / "catalog.json").read_text())["nodes"]
        for node in catalog:
            if node.get("gate") != "round1":
                continue
            proc = run(["progress", "tick", "--node", node["id"], "--status", "solid", "--format", "json"], data)
            check(proc.returncode == 0, f"solid {node['id']}", detail(proc))
        nxt = run(["practice", "next", "--format", "json"], data)
        nxt_doc = body(nxt)
        check(
            nxt.returncode == 0 and isinstance(nxt_doc, dict) and nxt_doc.get("id") is None and nxt_doc.get("reason") == "queue_clear",
            "a clear queue does not restart unit 1",
            detail(nxt),
        )

    with tempfile.TemporaryDirectory(prefix="ib-cli-mock-") as tmp:
        data = Path(tmp)
        opened = turn(data, {"kind": "mock-start", "cold": True, "id": "m1"})
        opened_doc = body(opened)
        check(opened.returncode == 0 and isinstance(opened_doc, dict) and opened_doc["session"]["phase"] == "mock_open", "cold mock opens", detail(opened))
        empty = turn(data, {"kind": "empty"})
        empty_doc = body(empty)
        check(
            empty.returncode == 0
            and isinstance(empty_doc, dict)
            and empty_doc["session"]["phase"] == "mock_open"
            and "still open" in empty_doc["say"]
            and "Do not start a new concept." in empty_doc["say"]
            and empty_doc.get("mock")
            and empty_doc.get("problems"),
            "empty continues the open mock",
            detail(empty),
        )
        again = turn(data, {"kind": "mock-start", "pack": "pdf-round1", "year": 2021})
        again_doc = body(again)
        check(
            again.returncode == 0
            and isinstance(again_doc, dict)
            and "stays" in again_doc["say"]
            and "repository" not in again_doc["say"]
            and any(row.get("id") == "SAMPLE-Q03" for row in again_doc.get("problems") or []),
            "a second pack leaves the open mock",
            detail(again),
        )
        finished = turn(data, {"kind": "mock-finish", "id": "m1", "score": 1, "out_of": 30})
        finished_doc = body(finished)
        check(
            finished.returncode == 0 and isinstance(finished_doc, dict) and finished_doc["session"]["phase"] == "idle",
            "finishing the open mock returns to idle",
            detail(finished),
        )

    with tempfile.TemporaryDirectory(prefix="ib-cli-clobber-") as tmp:
        data = Path(tmp)
        taught = turn(data, {"kind": "teach"})
        check(taught.returncode == 0 and body(taught)["session"]["phase"] == "awaiting_answer", "teach waits", detail(taught))
        sneak = run(["progress", "mock-start", "--cold", "--id", "sneak", "--format", "json"], data)
        check(sneak.returncode == 0, "cold mock record", detail(sneak))
        refused = turn(data, {"kind": "mock-finish", "id": "sneak", "score": 1, "out_of": 30})
        check(
            refused.returncode == 2 and "an integral is still open" in refused.stderr and "Traceback" not in refused.stderr,
            "mock-finish does not close an open integral",
            detail(refused),
        )
        session = json.loads((data / "session.json").read_text())
        mocks = json.loads((data / "mocks.json").read_text())
        check(session["phase"] == "awaiting_answer" and session["problem_id"] == "U01-D07", "the open drill is still stored", detail(refused))
        check(mocks["sessions"][0]["score"] is None, "the refused finish does not store a score", detail(refused))

    with tempfile.TemporaryDirectory(prefix="ib-cli-err-") as tmp:
        data = Path(tmp)
        missing = run(["turn", "apply", "--file", str(data / "missing.json"), "--format", "json"], data)
        check(
            missing.returncode == 2
            and "turn file not found:" in missing.stderr
            and "Traceback" not in missing.stderr
            and missing.stdout == ""
            and not any(data.iterdir()),
            "a missing turn file exits 2",
            detail(missing),
        )
        (data / "attempts.json").write_text("not-json\n")
        broken = run(["progress", "show", "--format", "json"], data)
        check(
            broken.returncode == 2 and "did not parse" in broken.stderr and "Traceback" not in broken.stderr,
            "corrupt attempts.json exits 2",
            detail(broken),
        )

    if fails:
        print(f"FAIL cli behavior ({len(fails)})")
        return 1
    print("PASS cli behavior")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
