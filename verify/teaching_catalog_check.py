#!/usr/bin/env python3
"""Check teaching coverage and evidence boundaries for the syllabus cards.

These checks use stored drill answers; the mathematical proof of those answers
remains in check_math.py. Mutations are in memory and never write learner state.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import sys

import yaml

import check_math
import gap_index
import turn_contract as turns

ROOT = Path(__file__).resolve().parent.parent

# The Round 1 gate before the seven syllabus cards were made ready (db203fa).
ROUND1 = frozenset({
    "basic-integration", "basic-u-substitution", "symmetry", "basic-exponential",
    "basic-trig-integrals", "basic-integration-by-parts", "basic-trig-substitution",
    "basic-partial-fractions", "area-partial-circle", "algebra-manipulation",
    "intermediate-u-substitution", "absolute-values", "reverse-product-rule",
    "basic-series", "intermediate-trig-integrals", "intermediate-trig-substitution",
    "inverse-functions", "kings-queens-rule", "gaussian-integrals", "special-wildcard",
})

LESSONS = {
    "floor": ("11-gaussian-wildcard", "docs/techniques/floor.md"),
    "dutis": ("34-frullani-feynman", "docs/techniques/introduce-constant.md"),
    "vector-calc": ("30-gaussian-dirichlet", "docs/techniques/concepts/vector-calc.md"),
    "beta": ("14-gamma", "docs/techniques/concepts/beta.md"),
    "zeta": ("35-modified-famous", "docs/techniques/concepts/zeta.md"),
    "euler-mascheroni": ("14-gamma", "docs/techniques/concepts/euler-mascheroni.md"),
    "catalan": ("36-unique-tricks", "docs/techniques/concepts/catalan.md"),
}
OPTIONAL = frozenset(LESSONS) - {"floor", "dutis"}
EVIDENCE = {
    "floor": [f"U11-D{n:02}" for n in range(9, 13)],
    "dutis": ["U11-D13", "U11-D14", "U11-D15", "U34-D04", "U34-D05"],
}
STAMP = "2026-10-27T08:00:00+08:00"


def catalog_errors(root: Path, nodes: list[dict], drills: list[dict]) -> list[str]:
    errors = []
    ids = [node["id"] for node in nodes]
    if len(ids) != 72 or len(set(ids)) != 72:
        errors.append("teaching catalog must contain 72 unique nodes")
    if {node["id"] for node in nodes if node.get("gate") == "round1"} != ROUND1:
        errors.append("Round 1 gate ids changed")
    known_drills = {drill["id"] for drill in drills}
    for node in nodes:
        ident = node["id"]
        if node.get("status") == "deferred":
            errors.append(f"{ident} remains deferred")
        if "drill_ids" not in node:
            continue
        evidence = node["drill_ids"]
        if not isinstance(evidence, list) or any(not isinstance(item, str) or not item for item in evidence):
            errors.append(f"{ident} drill_ids must be a list of nonempty ids")
            continue
        if len(set(evidence)) != len(evidence):
            errors.append(f"{ident} has duplicate explicit drill ids")
        unknown = set(evidence) - known_drills
        if unknown:
            errors.append(f"{ident} has unknown explicit drill ids: {sorted(unknown)}")
    by_id = {node["id"]: node for node in nodes}
    for ident, (unit, card) in LESSONS.items():
        node = by_id.get(ident, {})
        if node.get("status") != "ready" or node.get("unit") != unit or node.get("gate") is not None:
            errors.append(f"{ident} must be ready in {unit} with gate null")
        if node.get("drill_ids") != EVIDENCE.get(ident, []):
            errors.append(f"{ident} explicit practice evidence changed")
        for relative in (card, f"units/{unit}/teaching.tex"):
            path = root / relative
            if not path.is_file() or not path.read_text().strip():
                errors.append(f"{ident} missing lesson: {relative}")
        meta_path = root / "units" / unit / "meta.yaml"
        if not meta_path.is_file():
            errors.append(f"{ident} missing unit metadata")
            continue
        try:
            meta = yaml.safe_load(meta_path.read_text())
        except yaml.YAMLError:
            errors.append(f"{ident} unit metadata is invalid YAML")
            continue
        if meta.get("status") != "ready" or ident not in meta.get("technique_tags", []):
            errors.append(f"{ident} is not attached to its ready unit metadata")
    if by_id.get("floor", {}).get("teaching") != LESSONS["floor"][1]:
        errors.append("floor must retain its dedicated teaching note")
    return errors


def concept_map_errors(text: str, nodes: list[dict]) -> list[str]:
    """Compare inventory rows and reported counts, without freezing the prose."""
    groups = {
        "Round 1 nodes": [],
        "Later nodes with a coach card": [],
        "Unit lessons, no new example": [],
        "Official syllabus cards": [],
        "Deferred in the catalog": [],
        "Practice indexes": [],
    }
    errors = []
    reported = {}
    section = ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        match = re.fullmatch(r"`([a-z0-9-]+)`", cells[0])
        if match and section in groups:
            groups[section].append(match.group(1))
            if section == "Official syllabus cards" and cells[1] != "card":
                errors.append(f"{match.group(1)} syllabus depth must be card")
        if section == "Counts" and len(cells) == 2 and cells[1].isdigit():
            if cells[0] in reported:
                errors.append(f"duplicate concept-map count: {cells[0]}")
            reported[cells[0]] = int(cells[1])
    all_rows = [ident for rows in groups.values() for ident in rows]
    if Counter(all_rows) != Counter(node["id"] for node in nodes):
        errors.append("concept-map rows must list every catalog node exactly once")
    if set(groups["Round 1 nodes"]) != ROUND1:
        errors.append("concept-map Round 1 rows changed")
    if set(groups["Official syllabus cards"]) != set(LESSONS):
        errors.append("concept-map syllabus rows must contain the seven ready nodes")
    if groups["Deferred in the catalog"]:
        errors.append("concept-map still has deferred rows")
    observed = {
        "card, Round 1 gate": len(groups["Round 1 nodes"]),
        "card, later chapter or syllabus technique": len(groups["Later nodes with a coach card"]) + len(groups["Official syllabus cards"]),
        "unit lesson, no new example": len(groups["Unit lessons, no new example"]),
        "thin": 0,
        "deferred-taught": 0,
        "deferred-noted": 0,
        "deferred-open": 0,
        "index": len(groups["Practice indexes"]),
        "Total": len(all_rows),
    }
    if reported != observed:
        errors.append(f"concept-map counts do not match inventory: expected {observed}, got {reported}")
    if (observed["card, later chapter or syllabus technique"], observed["unit lesson, no new example"], observed["index"]) != (39, 4, 9):
        errors.append("concept-map depth inventory must be 39 later cards, 4 unit lessons, and 9 indexes")
    return errors


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def mark(node_id, drill, attempts, nodes, drills, answer=None):
    session = turns.empty_session()
    session.update(phase=turns.PHASE_AWAITING, node=node_id, problem_id=drill["id"])
    body = {
        "problem_id": drill["id"], "source": "typed",
        "extract": {"final_answer": drill["answer_sympy"] if answer is None else answer},
    }
    return turns.plan_mark(session, attempts, {}, nodes, drills, [], body, STAMP, catalog_rows=[])


def check_behavior(nodes: list[dict], drills: list[dict]) -> None:
    by_id = {node["id"]: node for node in nodes}
    drill_by_id = {drill["id"]: drill for drill in drills}
    for ident, expected in EVIDENCE.items():
        node = by_id[ident]
        require([row["id"] for row in turns.candidates_for(node, drills)] == expected, f"{ident} selection escaped its evidence list")
        unrelated_ids = ["U11-D01", "U11-D02"] if ident == "floor" else ["U34-D01", "U34-D02"]
        unrelated = [{"problem_id": pid, "correct": True} for pid in unrelated_ids]
        require(turns.distinct_correct(node, drills, unrelated) == 0, f"{ident} accepts unrelated host-unit successes")
        first = drill_by_id[expected[0]]
        # Exercise a cross-unit pair for DUTIS, not just its Unit 34 host.
        second = drill_by_id[expected[-1] if ident == "dutis" else expected[1]]
        attempt = {"problem_id": first["id"], "correct": True, "submitted": first["answer_sympy"]}
        require(turns.distinct_correct(node, drills, [attempt, attempt]) == 1, f"{ident} counts a duplicate twice")
        wrong = {"problem_id": second["id"], "correct": False}
        require(turns.distinct_correct(node, drills, [attempt, wrong]) == 1, f"{ident} counts a wrong answer")
        first_mark = mark(ident, first, [], nodes, drills)
        require(first_mark["exit"] == 0 and first_mark["tick"] is None, f"{ident} mastered after one correct answer")
        repeated = mark(ident, first, [attempt, attempt], nodes, drills)
        require(repeated["exit"] == 0 and repeated["tick"] is None, f"{ident} mastered after repeating one answer")
        missed = mark(ident, second, [attempt], nodes, drills, f"({second['answer_sympy']})+1")
        require(missed["exit"] == 1 and missed["tick"] is None, f"{ident} mastered after a wrong second answer")
        completed = mark(ident, second, [attempt], nodes, drills)
        require(completed["exit"] == 0 and completed["tick"] == {"node": ident, "status": "solid"}, f"{ident} failed two distinct correct answers")
    require("gaussian" not in turns.node_tags(by_id["floor"], drills), "floor inherited Gaussian weaknesses")
    require("frullani" not in turns.node_tags(by_id["dutis"], drills), "DUTIS inherited Frullani weaknesses")

    for ident in OPTIONAL:
        node = by_id[ident]
        host = [row for row in drills if row["unit"] == node["unit"]]
        require(len(host) >= 2, f"{ident} regression needs two host drills")
        attempts = [{"problem_id": row["id"], "correct": True} for row in host]
        require(turns.candidates_for(node, drills) == [], f"{ident} entered automatic practice")
        require(turns.pick_drill(node, drills, attempts) is None, f"{ident} inherited a host drill")
        require(turns.distinct_correct(node, drills, attempts) == 0, f"{ident} inherited host-unit mastery")
        require(turns.node_tags(node, drills) == set(), f"{ident} inherited host-unit weaknesses")
        require(ident not in turns.skip_offer(attempts, {}, nodes, drills), f"{ident} offered a skip for host-unit work")
        marked = mark(ident, host[1], attempts[:1], nodes, drills)
        require(marked["exit"] == 0 and marked["tick"] is None, f"{ident} ticked from two host answers")

    wildcard = {row["id"] for row in turns.candidates_for(by_id["special-wildcard"], drills)}
    expected_wildcard = {f"U11-D{n:02}" for n in [5, 6, 7, *range(9, 16)]}
    require(wildcard == expected_wildcard, "special-wildcard lost its existing floor or DUTIS routes")
    round1_ticks = {ident: {"status": "solid"} for ident in ROUND1}
    require(turns.readiness(nodes, round1_ticks)["ready"], "optional syllabus nodes block Round 1 readiness")
    del round1_ticks["special-wildcard"]
    require(turns.readiness(nodes, round1_ticks)["missing_round1"] == ["special-wildcard"], "Round 1 gate was weakened")
    ticks = {node["id"]: {"status": "solid"} for node in nodes if node["id"] not in OPTIONAL}
    heat = {"topics": {"gamma": {"attempts": 2, "fails": 1}, "advanced-gaussian": {"attempts": 2, "fails": 1}}}
    for full in (False, True):
        session = turns.empty_session()
        session["aptitude"]["full_coverage"] = full
        require(turns.recommend_node(nodes, ticks, heat, drills, full_coverage=full) is None, "completed queue recommends an oral lesson as a drill")
        plan = turns.plan_teach(session, [], ticks, nodes, drills, heat, STAMP, records=[])
        require(plan["exit"] == 0 and plan["error"] is None and plan["drill"] is None, "completed queue fails with no drill")
        require(plan["tick"] is None and plan["effects"] == {}, "completed queue wrote recognition mastery")

    index, error = gap_index.load_index(ROOT)
    require(not error and index is not None, "gap index did not load")
    floor = index.by_id("floor")
    require(floor is not None and floor.note == LESSONS["floor"][1], "floor gap lost its teaching note")
    require(gap_index._catalog_errors(index, nodes) == [], "ready floor conflicts with its gap route")
    require(LESSONS["floor"][1] in gap_index.note_say(by_id["floor"]["unit"], floor, False), "floor miss does not teach its note")


MUTATIONS = (
    "unknown-drill", "duplicate-drill", "duplicate-node", "deferred-node",
    "round1-expanded", "optional-inherits-drills", "floor-note", "stale-count",
)


def mutation_errors(name, nodes, drills, map_text) -> list[str]:
    changed = deepcopy(nodes)
    by_id = {node["id"]: node for node in changed}
    if name == "unknown-drill":
        by_id["floor"]["drill_ids"].append("U11-NO-SUCH-DRILL")
    elif name == "duplicate-drill":
        by_id["floor"]["drill_ids"].append("U11-D09")
    elif name == "duplicate-node":
        changed.append(deepcopy(by_id["beta"]))
    elif name == "deferred-node":
        by_id["beta"]["status"] = "deferred"
    elif name == "round1-expanded":
        by_id["beta"]["gate"] = "round1"
    elif name == "optional-inherits-drills":
        del by_id["beta"]["drill_ids"]
    elif name == "floor-note":
        by_id["floor"]["teaching"] = "units/11-gaussian-wildcard/teaching.tex"
        index, error = gap_index.load_index(ROOT)
        require(not error and index is not None, "gap index did not load for mutation")
        return gap_index._catalog_errors(index, changed)
    elif name == "stale-count":
        old = "| card, later chapter or syllabus technique | 39 |"
        require(old in map_text, "stale-count mutation did not target a count")
        return concept_map_errors(map_text.replace(old, old.replace("39", "38")), nodes)
    else:
        raise ValueError(f"unknown mutation {name}")
    return catalog_errors(ROOT, changed, drills)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-fail", choices=MUTATIONS)
    args = parser.parse_args()
    nodes = json.loads((ROOT / "trackers/catalog.json").read_text())["nodes"]
    drills = check_math.load_all_drills()
    map_text = (ROOT / "pedagogy/concept-map.md").read_text()
    try:
        errors = catalog_errors(ROOT, nodes, drills) + concept_map_errors(map_text, nodes)
        require(not errors, "; ".join(errors))
        if not args.expect_fail:
            check_behavior(nodes, drills)
            print("PASS teaching catalog: seven ready lessons, 72 nodes, unchanged 20-node Round 1 gate, consistent concept map")
            print("PASS teaching evidence: scoped floor/DUTIS drills, distinct-answer mastery, oral-only optional lessons, wildcard and gap routes")
        for name in [args.expect_fail] if args.expect_fail else MUTATIONS:
            errors = mutation_errors(name, nodes, drills, map_text)
            require(bool(errors), f"mutation {name} was accepted")
            print(f"PASS teaching mutation {name}")
    except (AssertionError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL teaching catalog: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
