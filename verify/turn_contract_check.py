#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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


def tracker_files(data: Path) -> dict:
    found = {}
    for path in sorted(data.glob("*.json")):
        if path.name == "turn.json":
            continue
        found[path.name] = path.read_text()
    return found


def drill_answers() -> dict[str, str]:
    answers = {}
    for path in sorted((ROOT / "verify").glob("drills_unit*.json")):
        for row in json.loads(path.read_text()):
            answers[row["id"]] = row["answer_sympy"]
    return answers


def placement(data: Path, check) -> None:
    schema = run(data, ["turn", "schema", "--format", "json"])
    check(
        schema.returncode == 0
        and all(word in schema.stdout for word in ("aptitude", "confirm", "cover", "proposing")),
        "schema names aptitude, confirm, cover, and proposing",
    )
    started = apply(data, {"kind": "aptitude"})
    started_doc = load(started)
    check(started.returncode == 0, "aptitude exit")
    check(started_doc["session"]["phase"] == "aptitude", "aptitude phase")
    check(started_doc["session"]["problem_id"] == "U01-D07", "aptitude opens U01-D07")
    check(started_doc["session"]["node"] == "basic-integration", "aptitude node is basic-integration")
    check(started_doc["drill"]["id"] == "U01-D07", "aptitude drill is U01-D07")
    check(started_doc["tick"] is None, "aptitude writes no tick")
    check("answer_display" not in started.stdout and "answer_sympy" not in started.stdout, "aptitude hides the drill answer")

    before_confirm = tracker_files(data)
    early = apply(data, {"kind": "confirm", "nodes": ["basic-integration"]})
    check(early.returncode == 2, "confirm before the offer exits 2")
    check(tracker_files(data) == before_confirm, "early confirm writes nothing")

    first_drill = apply(
        data,
        {
            "kind": "mark",
            "problem_id": "U01-D07",
            "source": "typed",
            "extract": {"final_answer": "0"},
        },
    )
    first_doc = load(first_drill)
    check(first_drill.returncode == 0, "U01-D07 aptitude mark exit")
    check(first_doc["tick"] is None or first_doc["tick"].get("status") != "skipped", "aptitude drill is not skipped")
    check(first_doc["session"]["phase"] == "aptitude", "a correct drill opens the contest probe")
    check(first_doc["session"]["problem_id"] == "R1-2020-Q19", "contest probe is R1-2020-Q19")
    check(first_doc["session"]["node"] is None, "contest probe has no node")
    check("answer_plain" not in first_drill.stdout, "contest probe hides answer_plain")
    policy = json.loads((data / "session.json").read_text())["policy"]["basic-integration"]
    check(set(policy) == {"approach", "detail", "kind", "volume"}, "basic-integration has a policy row")
    check(policy["detail"] == "faded" and policy["volume"] == 1, "a correct drill shortens the dosage")

    catalog_mark = apply(
        data,
        {
            "kind": "mark",
            "problem_id": "R1-2020-Q19",
            "source": "typed",
            "verdict": "correct",
            "extract": {"final_answer": "1"},
        },
    )
    catalog_doc = load(catalog_mark)
    check(catalog_mark.returncode == 0, "catalog probe mark exit")
    attempts = json.loads((data / "attempts.json").read_text())
    check(
        any(item["problem_id"] == "R1-2020-Q19" and item["correct"] is True for item in attempts["items"]),
        "catalog probe stores an attempt",
    )
    ticks = json.loads((data / "skill-ticks.json").read_text())["ticks"] if (data / "skill-ticks.json").exists() else {}
    check(ticks.get("basic-integration", {}).get("status") != "skipped", "catalog probe writes no skip")
    check(catalog_doc["tick"] is None, "catalog probe result tick is null")
    check(catalog_doc["session"]["phase"] == "proposing", "one evidenced node proposes a skip")
    check("basic-integration" in catalog_doc["coach"]["offer"], "basic-integration is offered")

    declined = apply(data, {"kind": "confirm", "nodes": []})
    check(declined.returncode == 0, "empty confirm declines")
    declined_doc = load(declined)
    check(declined_doc["session"]["phase"] == "idle", "decline returns to idle")
    declined_ticks = json.loads((data / "skill-ticks.json").read_text())["ticks"] if (data / "skill-ticks.json").exists() else {}
    check(declined_ticks.get("basic-integration", {}).get("status") != "skipped", "decline writes no skip")

    again = apply(data, {"kind": "aptitude"})
    again_doc = load(again)
    check(again.returncode == 0, "aptitude continues after a decline")
    check(again_doc["session"]["phase"] == "aptitude", "the next probe is open")
    check(again_doc["session"]["problem_id"] != "U01-D07", "a declined node is not probed again")
    check(again_doc["session"]["problem_id"] != "R1-2020-Q19", "the contest probe is not repeated")
    probe_id = again_doc["session"]["problem_id"]
    node_id = again_doc["session"]["node"]
    check(node_id and not str(probe_id).startswith("YANG-"), "the next probe is a unit drill")
    answers = drill_answers()
    marked = apply(
        data,
        {
            "kind": "mark",
            "problem_id": probe_id,
            "source": "typed",
            "extract": {"final_answer": answers[probe_id]},
        },
    )
    marked_doc = load(marked)
    check(marked.returncode == 0, "the next drill grades")
    check(marked_doc["session"]["phase"] == "proposing", "the next drill proposes its node")
    check("basic-integration" not in marked_doc["coach"]["offer"], "a declined node stays out of the offer")
    check(node_id in marked_doc["coach"]["offer"], "the new node is offered")

    before_bad = tracker_files(data)
    bad = apply(data, {"kind": "confirm", "nodes": [node_id, "symmetry"]})
    check(bad.returncode == 2, "confirm of an id outside the offer exits 2")
    check(tracker_files(data) == before_bad, "bad confirm writes nothing")

    confirmed = apply(data, {"kind": "confirm", "nodes": [node_id]})
    confirmed_doc = load(confirmed)
    check(confirmed.returncode == 0, "confirm the offered node")
    stored = json.loads((data / "skill-ticks.json").read_text())["ticks"]
    check(stored[node_id]["status"] == "skipped", "confirm writes skipped")
    check(stored.get("basic-integration", {}).get("status") != "skipped", "decline is still not a skip")
    check(confirmed_doc["coach"]["next_node"] != node_id, "skip leaves the coach queue")
    check(confirmed_doc["coach"]["ready"] is False, "a skip does not open the mock")
    blocked = apply(data, {"kind": "mock-start"})
    check(
        blocked.returncode == 2 and "round1 nodes not solid" in blocked.stderr,
        "mock stays blocked after a skip",
    )

    covered = apply(data, {"kind": "cover", "full": True})
    covered_doc = load(covered)
    check(covered.returncode == 0, "cover exit")
    covered_session = json.loads((data / "session.json").read_text())
    check(covered_session["aptitude"]["full_coverage"] is True, "cover sets full coverage")
    check(covered_doc["coach"]["full_coverage"] is True, "coach reports full coverage")
    missed = apply(
        data,
        {
            "kind": "mark",
            "problem_id": probe_id,
            "source": "typed",
            "extract": {"final_answer": "1"},
        },
    )
    check(missed.returncode == 1, "a miss on the skipped drill exits 1")
    cleared = json.loads((data / "skill-ticks.json").read_text())["ticks"][node_id]["status"]
    check(cleared == "learning", "a miss clears the skip")
    dosed = json.loads((data / "session.json").read_text())["policy"][node_id]
    check(dosed["detail"] == "worked", "a miss restores the worked dosage")


NOTE_PATHS = (
    "units/10-inverse-kings/teaching.tex",
    "units/20-wallis/teaching.tex",
    "units/26-weierstrass/teaching.tex",
    "docs/techniques/floor.md",
    "docs/techniques/introduce-constant.md",
    "docs/techniques/formats.md",
)


def note_hash() -> str:
    digest = hashlib.sha256()
    for rel in NOTE_PATHS:
        digest.update((ROOT / rel).read_bytes())
    return digest.hexdigest()


def reopen(data: Path, problem_id: str, node: str) -> None:
    session = json.loads((data / "session.json").read_text())
    session["phase"] = "awaiting_answer"
    session["problem_id"] = problem_id
    session["node"] = node
    session["mock_id"] = None
    (data / "session.json").write_text(json.dumps(session, indent=2) + "\n")


def gap_cases(data: Path, check) -> None:
    before = note_hash()
    missed = apply(
        data,
        {
            "kind": "mark",
            "problem_id": "U01-D07",
            "source": "typed",
            "extract": {"final_answer": "1", "gap": "floor", "method_note": "split the interval"},
        },
    )
    doc = load(missed)
    check(missed.returncode == 1, "floor miss exits 1")
    check("docs/techniques/floor.md" in doc["say"], "floor miss names floor.md")
    check("beyond-yang.md" not in doc["say"], "floor miss names one file")
    attempts = json.loads((data / "attempts.json").read_text())["items"]
    row = next(item for item in attempts if item["problem_id"] == "U01-D07")
    check(
        row["gap"] == "floor" and row["note"] == "final answer differed",
        "floor miss stores the gap id and the answer note",
    )
    check("split the interval" not in json.dumps(attempts), "a wrong answer drops method_note")
    journal = data / "journal.json"
    check(not journal.exists() or "split the interval" not in journal.read_text(), "a wrong answer writes no method journal")
    check(note_hash() == before, "a mark does not edit a teaching note")

    count = len(json.loads((data / "attempts.json").read_text())["items"])
    unknown = apply(
        data,
        {
            "kind": "mark",
            "problem_id": "U01-D08",
            "source": "typed",
            "extract": {"final_answer": "1", "gap": "batis"},
        },
    )
    check(unknown.returncode == 2 and "unknown gap" in unknown.stderr, "unknown gap exits 2")
    after_unknown = json.loads((data / "attempts.json").read_text())["items"]
    check(
        len(after_unknown) == count and not any(item["problem_id"] == "U01-D08" for item in after_unknown),
        "unknown gap writes nothing",
    )

    bare = apply(
        data,
        {
            "kind": "mark",
            "problem_id": "U26-D01",
            "source": "typed",
            "extract": {"final_answer": "1", "gap": "weierstrass"},
        },
    )
    check(
        bare.returncode == 2 and "correct mark needs method_note when gap is set" in bare.stderr,
        "correct gap without method_note exits 2",
    )
    check(
        not any(
            item["problem_id"] == "U26-D01"
            for item in json.loads((data / "attempts.json").read_text())["items"]
        ),
        "correct gap without method_note writes nothing",
    )

    method = apply(
        data,
        {
            "kind": "mark",
            "problem_id": "U26-D01",
            "source": "typed",
            "extract": {"final_answer": "1", "gap": "weierstrass", "method_note": "half angle"},
        },
    )
    method_doc = load(method)
    check(method.returncode == 0, "weierstrass method gap exits 0")
    check("units/26-weierstrass/teaching.tex" in method_doc["say"], "method gap names the unit note")
    marks = json.loads((data / "marks.json").read_text())["marks"]["U26-D01"]
    check(marks["method_ok"] is False and marks["answer_ok"] is True, "method gap keeps method_ok false")
    stored = next(
        item
        for item in json.loads((data / "attempts.json").read_text())["items"]
        if item["problem_id"] == "U26-D01"
    )
    check(stored["gap"] == "weierstrass", "method gap stores the id")

    contest = apply(
        data,
        {
            "kind": "mark",
            "problem_id": "R1-2024-Q01",
            "source": "typed",
            "extract": {"final_answer": "0"},
        },
    )
    contest_doc = load(contest)
    check(
        contest.returncode == 1 and contest_doc["say"] == "The final answer does not match.",
        "a contest miss with no unit names no note",
    )
    check("teaching.tex" not in contest_doc["say"], "a contest miss does not invent teaching.tex")

    fresh = data / "retry"
    fresh.mkdir()
    first = apply(
        fresh,
        {
            "kind": "mark",
            "problem_id": "U01-D07",
            "source": "typed",
            "extract": {"final_answer": "1"},
        },
    )
    check(first.returncode == 1, "open retry starts from a recorded miss")
    reopen(fresh, "U01-D07", "basic-integration")
    filled = apply(
        fresh,
        {
            "kind": "mark",
            "problem_id": "U01-D07",
            "source": "typed",
            "extract": {"final_answer": "1", "gap": "floor"},
        },
    )
    filled_doc = load(filled)
    filled_items = json.loads((fresh / "attempts.json").read_text())["items"]
    check(filled.returncode == 1 and len(filled_items) == 1, "an open retry does not append")
    check(filled_items[0].get("gap") == "floor", "an open retry fills the stored gap")
    check("already recorded" in filled_doc["say"] and "docs/techniques/floor.md" in filled_doc["say"], "the fill names the recorded line and the note")
    reopen(fresh, "U01-D07", "basic-integration")
    refused = apply(
        fresh,
        {
            "kind": "mark",
            "problem_id": "U01-D07",
            "source": "typed",
            "extract": {"final_answer": "1", "gap": "reflection"},
        },
    )
    refused_items = json.loads((fresh / "attempts.json").read_text())["items"]
    check(refused.returncode == 2 and "gap does not match the recorded gap" in refused.stderr, "an open retry refuses a different gap")
    check(len(refused_items) == 1 and refused_items[0].get("gap") == "floor", "a refused retry leaves the stored gap")
    check(note_hash() == before, "gap marks leave the notes unchanged")


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
        check(
            set(schema_doc["request"]["kinds"])
            == {"empty", "teach", "mark", "mock-start", "mock-finish", "aptitude", "confirm", "cover"},
            "schema kinds match",
        )
        check(set(schema_doc["result"]["phases"]) == model.SESSION_PHASES, "schema phases match")
        check(schema_doc["request"]["confirm"]["required"] == ["kind", "nodes"], "confirm requires nodes")
        check(
            schema_doc["request"]["mark"].get("extract_optional") == ["method_note", "gap"],
            "mark extract may name a gap",
        )

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
        check(
            "units/01-foundations-substitution/teaching.tex" in wrong_doc["say"],
            "a unit miss names the unit note",
        )
        check("beyond-yang.md" not in wrong_doc["say"], "a unit miss does not name the index")
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
        marks = json.loads((data / "marks.json").read_text())
        gap = marks["marks"]["U01-D07"]
        check(gap["answer_ok"] is True and gap["method_ok"] is False, "method gap is a mark row")
        check(gap["note"] == "odd integrand" and gap["technique"] == "odd-even", "mark row names the technique")
        clean = marks["marks"]["U01-D08"]
        check(clean["answer_ok"] is True and clean["method_ok"] is True, "a clean mark stores both facts")
        cards = json.loads((data / "stickies.json").read_text())
        check(cards["cards"]["odd-even"]["note"] == "odd integrand", "method gap is the technique card")
        check("strength" not in cards["cards"]["odd-even"], "sticky strength is not stored")
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
        q01 = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q01",
                "source": "typed",
                "extract": {"final_answer": "log(6)"},
            },
        )
        check(q01.returncode == 0 and load(q01)["mark"]["correct"] is True, "SAMPLE-Q01 grades with SymPy")
        q17 = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q17",
                "source": "photo",
                "extract": {"final_answer": "E*x+C"},
            },
        )
        check(q17.returncode == 0 and load(q17)["mark"]["correct"] is True, "SAMPLE-Q17 accepts e*x+C")
        suspect = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q17",
                "source": "typed",
                "extract": {"final_answer": "log(Abs(log(x)))+C"},
            },
        )
        check(suspect.returncode == 1 and load(suspect)["mark"]["correct"] is False, "SAMPLE-Q17 rejects ln|ln x|+C")
        printed = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q15",
                "source": "typed",
                "extract": {
                    "final_answer": "log(x + 1)/3 - (log(x**2 - x + 1) + 2*sqrt(3)*atan((2*x - 1)/sqrt(3)))/6"
                },
            },
        )
        check(printed.returncode == 1 and load(printed)["mark"]["correct"] is False, "SAMPLE-Q15 rejects the printed sign")
        manual = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q05",
                "source": "photo",
                "extract": {"final_answer": "pi*log(2)/8"},
                "verdict": "correct",
            },
        )
        check(manual.returncode == 0 and load(manual)["mark"]["correct"] is True, "manual verdict can be correct")
        bare = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "SAMPLE-Q09",
                "source": "typed",
                "extract": {"final_answer": "1/2 - zeta(3)/3"},
            },
        )
        check(bare.returncode == 2 and "manual problem needs verdict" in bare.stderr, "manual mark without a verdict writes nothing")
        attempts = json.loads((data / "attempts.json").read_text())
        check(not any(item["problem_id"] == "SAMPLE-Q09" for item in attempts["items"]), "refused manual mark is absent")

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
        check(pdf_doc["problems"][0]["count"] == 40 and pdf_doc["problems"][0]["on_disk"] is True, "2021 is a 40-question paper and the committed PDF is on disk")
        check("repository" not in pdf_doc["say"], "the mock line does not mention the repository")

        refused = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "R1-2023-Q05",
                "source": "typed",
                "extract": {"final_answer": "0"},
            },
        )
        check(refused.returncode == 2 and "manual problem needs verdict" in refused.stderr, "catalog mark needs a verdict")
        attempts_doc = json.loads((data / "attempts.json").read_text())
        before = len(attempts_doc["items"])
        check(not any(item["problem_id"] == "R1-2023-Q05" for item in attempts_doc["items"]), "refused catalog mark writes no attempt")
        accepted = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "R1-2023-Q05",
                "source": "typed",
                "verdict": "correct",
                "extract": {"final_answer": "not-a-sympy-expression"},
            },
        )
        accepted_doc = load(accepted)
        check(accepted.returncode == 0 and accepted_doc["mark"]["correct"] is True, "manual catalog mark stores the verdict")
        check(accepted_doc["mark"]["expected_display"] == "0", "manual mark shows the cited answer")
        shown = run(data, ["progress", "show", "--format", "json"])
        check("R1-2023-Q05" in shown.stdout, "progress show reads the catalog attempt")
        after = json.loads((data / "attempts.json").read_text())
        check(len(after["items"]) == before + 1, "catalog mark appends one attempt")
        gated = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "R1-2024-Q01",
                "source": "typed",
                "extract": {"final_answer": "sin(1)"},
            },
        )
        gated_doc = load(gated)
        check(gated.returncode == 0 and gated_doc["mark"]["correct"] is True, "sympy catalog mark needs no verdict")
        overridden = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "R1-2024-Q01",
                "source": "typed",
                "verdict": "correct",
                "extract": {"final_answer": "0"},
            },
        )
        overridden_doc = load(overridden)
        check(overridden.returncode == 1 and overridden_doc["mark"]["correct"] is False, "a verdict cannot override a wrong sympy answer")
        for problem_id, final, correct in (
            ("R1-2023-Q04", "2*x*X+C", True),
            ("R1-2023-Q04", "2*x*X+sin(x)", True),
            ("R1-2023-Q04", "2*x*X+X", False),
            ("R1-2024-Q10", "sqrt(pi)*exp(-x**2)/2", True),
            ("R1-2024-Q10", "sqrt(pi)*exp(-t**2)/2", False),
        ):
            marked = apply(
                data,
                {
                    "kind": "mark",
                    "problem_id": problem_id,
                    "source": "typed",
                    "extract": {"final_answer": final},
                },
            )
            check(
                marked.returncode == (0 if correct else 1) and load(marked)["mark"]["correct"] is correct,
                f"{problem_id} grades {final} with its integration variable",
            )
        invented = apply(
            data,
            {
                "kind": "mark",
                "problem_id": "YANG-1.1-P01",
                "source": "typed",
                "verdict": "correct",
                "extract": {"final_answer": "x"},
            },
        )
        check(invented.returncode == 2 and "no printed answer" in invented.stderr, "unanswered yang practice is not graded")
        check("YANG-1.1-P01" not in run(data, ["progress", "show", "--format", "json"]).stdout, "yang practice leaves no attempt")

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
    filled = turn_contract.plan_mark(
        session,
        attempts,
        {},
        [],
        drills,
        [],
        {
            "kind": "mark",
            "problem_id": "U01-D07",
            "source": "photo",
            "extract": {"final_answer": "1", "gap": "floor", "method_note": "do not store"},
        },
        "t3",
    )
    check(
        filled["exit"] == 1
        and filled["effects"] == {"gap_fill": {"problem_id": "U01-D07", "gap": "floor"}}
        and "attempt" not in filled["effects"],
        "an open miss can record the gap without a second attempt",
    )
    check("docs/techniques/floor.md" in filled["say"], "the fill names the floor note")
    rejected = turn_contract.plan_mark(
        session,
        [{"problem_id": "U01-D07", "correct": False, "submitted": "1", "gap": "floor"}],
        {},
        [],
        drills,
        [],
        {
            "kind": "mark",
            "problem_id": "U01-D07",
            "source": "photo",
            "extract": {"final_answer": "1", "gap": "reflection"},
        },
        "t4",
    )
    check(
        rejected["exit"] == 2 and rejected["error"] == "gap does not match the recorded gap",
        "a different gap on the open mark is refused",
    )
    check(rejected["effects"] == {}, "a refused gap writes no effect")
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

    with tempfile.TemporaryDirectory() as tmp:
        placement(Path(tmp), check)

    with tempfile.TemporaryDirectory() as tmp:
        gap_cases(Path(tmp), check)

    if fail:
        print("FAIL turn contract")
        return 1
    print("PASS turn contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
