#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))

import model  # noqa: E402
import turn_contract  # noqa: E402

CLI = ROOT / "scripts" / "control-integration-bee"


def run(data: Path, args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["IB_DATA_DIR"] = str(data)
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        input=stdin,
        text=True,
        capture_output=True,
        env=env,
        cwd=ROOT,
    )


def apply(data: Path, body: dict) -> subprocess.CompletedProcess:
    path = data / "turn.json"
    path.write_text(json.dumps(body))
    return run(data, ["turn", "apply", "--file", str(path), "--format", "json"])


def load(proc: subprocess.CompletedProcess) -> dict:
    return json.loads(proc.stdout)


def main() -> int:
    fail = 0

    def check(cond: bool, label: str) -> None:
        nonlocal fail
        if cond:
            print(f"OK {label}")
        else:
            print(f"FAIL {label}")
            fail = 1

    with tempfile.TemporaryDirectory() as tmp:
        data = Path(tmp)
        schema = run(data, ["turn", "schema", "--format", "json"])
        check(schema.returncode == 0, "schema exit")
        schema_doc = load(schema)
        check("mark" in schema_doc["request"]["kinds"], "schema lists mark")
        check("awaiting_answer" in schema_doc["result"]["phases"], "schema lists awaiting_answer")

        shown = run(data, ["turn", "show", "--format", "json"])
        show_doc = load(shown)
        check(shown.returncode == 0 and show_doc["session"]["phase"] == "idle", "show starts idle")
        files_after_show = list(data.glob("*.json"))
        check(files_after_show == [], "show writes nothing")

        empty = apply(data, {"kind": "empty"})
        empty_doc = load(empty)
        check(empty.returncode == 0 and empty_doc["coach"]["next_node"] == "basic-integration", "empty names basic-integration")
        check(empty_doc["coach"]["ready"] is False, "round 1 is not ready")

        first = apply(data, {"kind": "teach"})
        first_doc = load(first)
        check(first.returncode == 0, "teach exit")
        check(first_doc["session"]["phase"] == "awaiting_answer", "teach waits for an answer")
        check(first_doc["drill"]["id"] == "U01-D07", "teach serves U01-D07")
        check("answer_display" not in first_doc["drill"], "teach hides the answer")
        check("answer_sympy" not in json.dumps(first_doc["drill"]), "teach hides sympy")
        check(first_doc["tick"]["status"] == "learning", "teach marks the node learning")
        again = apply(data, {"kind": "teach"})
        again_doc = load(again)
        check(again_doc["drill"]["id"] == "U01-D07" and again_doc["tick"] is None, "second teach repeats the open drill")

        wrong = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "U01-D07",
                "source": "photo",
                "extract": {"final_answer": "1"},
            },
        )
        wrong_doc = load(wrong)
        check(wrong.returncode == 1 and wrong_doc["mark"]["correct"] is False, "wrong photo mark fails closed")
        check(wrong_doc["session"]["phase"] == "idle", "wrong mark closes the drill")
        heat = json.loads((data / "heatmap.json").read_text())
        check(heat["topics"]["yang:1.1"]["fails"] == 1, "wrong mark bumps the heatmap")
        show = load(run(data, ["progress", "show", "--format", "json"]))
        check(any(row["problem_id"] == "U01-D07" and row["correct"] is False for row in show["attempts"]), "progress show reads the miss")

        nxt = load(apply(data, {"kind": "teach"}))
        check(nxt["drill"]["id"] == "U01-D08", "next teach skips the miss")
        good = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "U01-D08",
                "source": "typed",
                "extract": {"final_answer": "pi/4"},
            },
        )
        good_doc = load(good)
        check(good.returncode == 0 and good_doc["mark"]["correct"] is True, "U01-D08 matches pi/4")
        third = load(apply(data, {"kind": "teach"}))
        check(third["drill"]["id"] == "U01-D07", "the missed drill comes back")
        solid = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "U01-D07",
                "source": "typed",
                "extract": {"final_answer": "0", "method_note": "odd integrand"},
            },
        )
        solid_doc = load(solid)
        check(solid.returncode == 0 and solid_doc["tick"]["status"] == "solid", "two correct drills make the node solid")
        notes = json.loads((data / "journal.json").read_text())
        check(any(note["note"] == "odd integrand" for note in notes["notes"]), "method note is a journal entry")
        ticks = json.loads((data / "skill-ticks.json").read_text())
        check(ticks["ticks"]["basic-integration"]["status"] == "solid", "solid tick is stored")

        blocked = apply(data, {"kind": "mock-start"})
        check(blocked.returncode == 2 and "round1 nodes not solid" in blocked.stderr, "mock stays blocked")
        cold = apply(data, {"kind": "mock-start", "cold": True, "id": "mock-cold"})
        cold_doc = load(cold)
        check(cold.returncode == 0 and cold_doc["session"]["phase"] == "mock_open", "cold mock opens")
        again_pack = apply(data, {"kind": "mock-start", "pack": "pdf-round1", "year": 2021})
        check(
            again_pack.returncode == 0 and any(row["id"] == "SAMPLE-Q03" for row in load(again_pack)["problems"]),
            "a second mock start keeps the open pack",
        )
        check(any(row["id"] == "SAMPLE-Q03" for row in cold_doc["problems"]), "cold mock lists SAMPLE-Q03")
        check("duration_minutes" in cold_doc and cold_doc["duration_minutes"] == 120, "mock carries 120 minutes")

        sample = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q03",
                "source": "photo",
                "extract": {"final_answer": "pi/4"},
            },
        )
        check(sample.returncode == 0 and load(sample)["mark"]["correct"] is True, "SAMPLE-Q03 grades with SymPy")
        q17 = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q17",
                "source": "photo",
                "extract": {"final_answer": "log(Abs(log(x)))+C"},
            },
        )
        check(q17.returncode == 0 and load(q17)["mark"]["correct"] is True, "SAMPLE-Q17 accepts ln|ln x|+C")
        suspect = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q17",
                "source": "typed",
                "extract": {"final_answer": "exp(x)+C"},
            },
        )
        check(suspect.returncode == 1 and load(suspect)["mark"]["correct"] is False, "SAMPLE-Q17 rejects the PDF misprint")
        manual = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q01",
                "source": "photo",
                "extract": {"final_answer": "ln 6"},
                "verdict": "correct",
            },
        )
        check(manual.returncode == 0 and load(manual)["mark"]["correct"] is True, "manual verdict can be correct")
        bare = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q02",
                "source": "typed",
                "extract": {"final_answer": "pi/2"},
            },
        )
        check(bare.returncode == 2 and "manual problem needs verdict" in bare.stderr, "manual mark without a verdict writes nothing")
        attempts = json.loads((data / "attempts.json").read_text())
        check(not any(item["problem_id"] == "SAMPLE-Q02" for item in attempts["items"]), "refused manual mark is absent")

        indef = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "U01-D06",
                "source": "photo",
                "extract": {"final_answer": "log(Abs(x**2+3*x+2))+C"},
            },
        )
        check(indef.returncode == 0 and load(indef)["mark"]["correct"] is True, "indefinite photo may include +C")
        shifted = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "U01-D08",
                "source": "typed",
                "extract": {"final_answer": "pi/4+1"},
            },
        )
        check(shifted.returncode == 1 and load(shifted)["mark"]["correct"] is False, "a definite answer rejects an added constant")

        done = apply(data, {"kind": "mock-finish", "id": "mock-cold", "score": 1, "out_of": 30, "missed": ["SAMPLE-Q01"]})
        check(done.returncode == 0 and load(done)["session"]["phase"] == "idle", "mock finish returns to idle")

        cat = json.loads((ROOT / "trackers" / "catalog.json").read_text())["nodes"]
        for node in cat:
            if node.get("gate") == "round1" and node["id"] != "basic-integration":
                proc = run(
                    data,
                    ["progress", "tick", "--node", node["id"], "--status", "solid", "--format", "json"],
                )
                if proc.returncode != 0:
                    check(False, f"tick {node['id']}")
                    break
        opened = apply(data, {"kind": "mock-start", "id": "mock-ready"})
        check(opened.returncode == 0 and load(opened)["mock"]["cold"] is False, "solid round 1 opens a mock")
        apply(data, {"kind": "mock-finish", "id": "mock-ready", "score": 2, "out_of": 30})
        pdf = apply(data, {"kind": "mock-start", "pack": "pdf-round1", "year": 2021, "id": "mock-2021"})
        pdf_doc = load(pdf)
        check(pdf.returncode == 0 and pdf_doc["problems"][0]["year"] == 2021, "a year selects the 2021 paper")
        check(pdf_doc["problems"][0]["count"] == 40 and pdf_doc["problems"][0]["on_disk"] is False, "2021 stays a 40-question paper when the PDF is absent")
        check("repository" not in pdf_doc["say"], "the mock line does not mention the repository")

        projection = json.loads((data / "progress.local.json").read_text())
        check(projection["session"]["phase"] == "mock_open", "projection stores the session")
        check(any(row["problem_id"] == "U01-D07" for row in projection["mistakes"]), "projection stores the miss")

    session = {"schema": "integration-bee-session/v1", "phase": "awaiting_answer", "node": "basic-integration", "problem_id": "U01-D07", "mock_id": None, "updated": "t"}
    attempts = [{"problem_id": "U01-D07", "correct": False, "submitted": "1"}]
    drills = json.loads((ROOT / "verify" / "drills_unit1.json").read_text())
    plan = turn_contract.plan_mark(
        session,
        attempts,
        {},
        [],
        drills,
        [],
        {"kind": "mark", "problem_id": "U01-D07", "source": "photo", "extract": {"final_answer": "1"}},
        "t2",
    )
    check(plan["mark"]["idempotent"] is True and plan["effects"] == {}, "a repeated open mark does not append")
    check(plan["session"]["phase"] == "idle", "the repeated mark closes the drill")
    check(model.session_problem({"phase": "nope"}) == "bad session phase", "bad phase is a session error")
    weak = turn_contract.recommend_node(
        [
            {"id": "basic-integration", "unit": "01-foundations-substitution", "status": "ready", "yang": "1.1", "gate": "round1"},
            {"id": "basic-u-substitution", "unit": "01-foundations-substitution", "status": "ready", "yang": "1.2", "gate": "round1"},
        ],
        {},
        {"topics": {"u-sub": {"attempts": 2, "fails": 2}}},
        json.loads((ROOT / "verify" / "drills_unit1.json").read_text()),
    )
    check(weak is not None and weak["id"] == "basic-u-substitution", "a weak tag beats catalog order")

    if fail:
        print("FAIL turn contract")
        return 1
    print("PASS turn contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
