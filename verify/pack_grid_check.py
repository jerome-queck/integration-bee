"""Behavioral controls for source-bound crossnumber proof and marking."""

from copy import deepcopy
from importlib import import_module
import json

import pack_gate
import pack_grid
import problem_catalog
import turn_contract


HELD = {
    "R2-2021-Crossnumber-Across-1",
    "R2-2021-Crossnumber-Down-1",
    "R2-2023-Crossnumber-Down-1",
}


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def rejected(row, answer, label, source=None):
    require(not pack_gate.proven("grid", source or row["sympy_expr"], [], answer, "grid"), label)


def check_promoted(row):
    ident = row["id"]
    values = pack_grid.answer_map(row["answer_sympy"])
    require(values is not None, ident + " answer map")
    fields = pack_gate.fields_from_parts(row["sympy_expr"], None, row["answer_sympy"], "grid")
    require(fields is not None and all(row[key] == value for key, value in fields.items()),
            ident + " source and answer round-trip")
    reordered = json.dumps(list(reversed(list(values.items()))))
    require(pack_gate.proven("grid", row["sympy_expr"], None, reordered, "grid"),
            ident + " pair order does not change the answer")

    for key, value in values.items():
        changed = dict(values)
        changed[key] = value + (1 if value % 10 != 9 else -1)
        rejected(row, pack_grid.answer_text(changed), f"{ident} changed clue {key}")

    first = next(iter(values))
    for answer in (
        "{}", "[]", str(values[first]), "".join(str(v) for v in values.values()),
        json.dumps({str(k): v for k, v in values.items() if k != first}),
        pack_grid.answer_text({**values, 999: 1}),
        '{"%s":%s,"%s":%s}' % (first, values[first], first, values[first]),
        '[[%s,%s],[%s,%s]]' % (first, values[first], first, values[first]),
        '{"%s":true}' % first, '{"%s":%s.0}' % (first, values[first]),
        '{"%s":-1}' % first, '{"%s":"%s"}' % (first, values[first]),
        '{"0%s":%s}' % (first, values[first]), "not-json", row["answer_sympy"] + "+C",
    ):
        rejected(row, answer, ident + " rejects malformed or incomplete answer")

    source = json.loads(row["sympy_expr"])
    label = ("A" if source["direction"] == "across" else "D") + str(first)
    mutations = []
    changed = deepcopy(source)
    changed["clues"][label] += " + 1"
    mutations.append(changed)
    changed = deepcopy(source)
    del changed["clues"][label]
    mutations.append(changed)
    changed = deepcopy(source)
    changed["selection"] = []
    mutations.append(changed)
    changed = deepcopy(source)
    changed["selection"][0] = float(changed["selection"][0])
    mutations.append(changed)
    changed = deepcopy(source)
    changed["starts"][label][0] += 1
    mutations.append(changed)
    changed = deepcopy(source)
    changed["problem_pdf"] = changed["mark_pdf"]
    mutations.append(changed)
    for changed in mutations:
        rejected(row, row["answer_sympy"], ident + " rejects altered source", json.dumps(changed))

    for field, value in (
        ("id", "invented-grid-row"), ("problem_id", "Wrong-999"), ("year", "1900"),
        ("region", "elsewhere"), ("round", "r1"), ("pdf_role", "answers"),
        ("answer_plain", "999"), ("integrand_plain", "truncated OCR"),
        ("answer_latex", "999"), ("variable", "x"), ("limits", ["0", "1"]),
    ):
        require(pack_gate.reprove_rows([dict(row, **{field: value})]) is not None,
                ident + " rejects " + field + " drift")

    for submitted, expected in ((row["answer_sympy"], True), (reordered, True),
                                ("{}", False), (str(values[first]), False),
                                (pack_grid.answer_text({**values, first: values[first]+1}), False)):
        graded, error = turn_contract.grade_problem(ident, submitted, None, [], [], [row])
        require(error is None and graded["correct"] is expected and not graded["manual"],
                ident + " marks a structured answer")
        require(turn_contract.answer_matches(graded["row"], submitted) is expected,
                ident + " rechecks the stored attempt")


def check_siblings(rows):
    by_id = {row["id"]: row for row in rows}
    across = by_id["R2-2022-Crossnumber-Across-1"]
    down = by_id["R2-2022-Crossnumber-Down-1"]
    copied = dict(down, id=across["id"])
    require(pack_gate.reprove_rows([copied]) is not None, "cannot copy a sibling certificate to another row")
    manual_sibling = dict(down, kind="indefinite", verify="manual",
                          answer_plain=down["answer_plain"].replace("13579", "13578"))
    require(pack_gate.reprove_rows([across, manual_sibling]) is not None,
            "a manual sibling cannot contradict checked crossings")
    wrong = pack_grid.answer_map(down["answer_sympy"])
    wrong[1] += 1
    require(pack_gate.reprove_rows([across, dict(down, answer_sympy=pack_grid.answer_text(wrong))]) is not None,
            "a proved sibling cannot contradict checked crossings")


def check_math_is_executed():
    for puzzle, label in (("2022", "A7"), ("2023", "A11"), ("2024", "D5"), ("2025-UK", "D1")):
        module = import_module(pack_grid.SOURCES[puzzle].module)
        across, down = dict(module.ACROSS), dict(module.DOWN)
        require(module.checks(across, down)[label]() is True, puzzle + " integral certificate")
        values = across if label[0] == "A" else down
        values[int(label[1:])] += 1
        require(module.checks(across, down)[label]() is False,
                puzzle + " integral certificate rejects a false value independently of grid equality")


def check_all(rows=None):
    rows = rows or problem_catalog.load_records()
    targets = {ident for source in pack_grid.SOURCES.values() for ident in (source.across_id, source.down_id)}
    selected = [row for row in rows if row["id"] in targets]
    require(len(selected) == 12, "twelve Handoff G target rows")
    require(pack_gate.PROOF_TIMEOUT == 20.0, "ordinary proof timeout is unchanged")
    require(pack_gate.reprove_rows(selected) is None, "crossnumber catalog reproof and sibling consistency")
    for row in selected:
        if row["id"] in HELD:
            require(row["verify"] == "manual" and "answer_sympy" not in row,
                    row["id"] + " unresolved source stays manual")
            for puzzle, source in pack_grid.SOURCES.items():
                if row["id"] not in (source.across_id, source.down_id):
                    continue
                direction = "across" if row["id"] == source.across_id else "down"
                module = import_module(source.module)
                values = module.ACROSS if direction == "across" else module.DOWN
                require(not pack_gate.proven("grid", pack_grid.problem_text(puzzle, direction), [],
                                             pack_grid.answer_text(values), "grid"),
                        row["id"] + " marked digits alone do not pass")
        else:
            require(row["verify"] == "sympy" and row["kind"] == "grid", row["id"] + " promoted map")
            check_promoted(row)
    check_siblings(selected)
    check_math_is_executed()
    print("PASS crossnumber contract (nine proved maps, three source holds, wrong answers, source mutations, siblings, marking)")


if __name__ == "__main__":
    check_all()
