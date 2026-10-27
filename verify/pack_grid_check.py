"""Behavioral controls for source-bound crossnumber proof and marking."""

from copy import deepcopy
from importlib import import_module
import json

import pack_gate
import pack_grid
import problem_catalog
import turn_contract


RESOLVED_CLUES = {
    "R2-2021-Crossnumber-Across-1": {"A8"},
    "R2-2021-Crossnumber-Down-1": {"D3", "D4"},
    "R2-2023-Crossnumber-Down-1": {"D7"},
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
    for puzzle, label in (("2021", "A8"), ("2021", "D3"), ("2021", "D4"),
                          ("2022", "A7"), ("2023", "A11"), ("2023", "D7"),
                          ("2024", "D5"), ("2025-UK", "D1")):
        module = import_module(pack_grid.SOURCES[puzzle].module)
        across, down = dict(module.ACROSS), dict(module.DOWN)
        require(module.checks(across, down)[label]() is True, puzzle + " integral certificate")
        values = across if label[0] == "A" else down
        values[int(label[1:])] += 1
        require(module.checks(across, down)[label]() is False,
                puzzle + " integral certificate rejects a false value independently of grid equality")


def check_clarifications(rows):
    for row in rows:
        source = json.loads(row["sympy_expr"])
        expected = RESOLVED_CLUES.get(row["id"], set())
        require(set(source.get("clarifications", {})) == expected,
                row["id"] + " only selected clues carry grading clarifications")
        if not expected:
            continue
        prompt = problem_catalog.prompt_view(row)
        require("answer_sympy" not in prompt and "answer_plain" not in prompt,
                row["id"] + " clarified learner prompt hides the answer map")
        changed = deepcopy(source)
        del changed["clarifications"]
        rejected(row, row["answer_sympy"], row["id"] + " unqualified printed clue is not certified",
                 json.dumps(changed))
        changed = deepcopy(source)
        changed["clarifications"]["A999"] = "An unrelated grading convention."
        rejected(row, row["answer_sympy"], row["id"] + " rejects misplaced clarification",
                 json.dumps(changed))
        for label in expected:
            require(source["clarifications"][label] in prompt["integrand_plain"],
                    row["id"] + " learner sees " + label + " clarification")
            for replacement in (None, "", "No additional assumption or convention."):
                changed = deepcopy(source)
                if replacement is None:
                    del changed["clarifications"][label]
                else:
                    changed["clarifications"][label] = replacement
                rejected(row, row["answer_sympy"], row["id"] + " rejects changed " + label + " convention",
                         json.dumps(changed))
        if "D7" in expected:
            changed = deepcopy(source)
            changed["clarifications"]["D7"] = "For grading Down 7, f is absolutely integrable on [-1,1]."
            rejected(row, row["answer_sympy"], "D7 cannot omit continuity at zero",
                     json.dumps(changed))


def check_contest_readings():
    module = import_module("pack_grid_2021")
    across, down = dict(module.ACROSS), dict(module.DOWN)
    checks = module.checks(across, down)
    # These alternative readings are mathematically different, even before
    # the fixed lattice is considered. Do not quietly reintroduce either one.
    for index in (pow(7, down[9], down[7]) + 1, down[9] % down[7] + 1):
        down[3] = index * (index + 1) // 2
        require(checks["D3"]() is False, "D3 rejects the ungrouped and handoff-shorthand readings")
    down[3] = module.DOWN[3]
    across[8] = 1867
    require(checks["A8"]() is False, "A8 uses the journal-volume year, not the pamphlet year")
    # Same palindrome and digit product as the mark, but wrong residue:
    # 2*1*7*9*7*1*2=1764 and digit sum 29 == 2 (mod 9).
    for answer, label in ((2179712, "digit-sum congruence"),
                           (7134371, "palindrome"), (7126217, "digit product")):
        down[4] = answer
        require(checks["D4"]() is False, "D4 independently enforces the " + label)
    down[4] = module.DOWN[4]
    down[9] += 1
    require(checks["D3"]() is False, "D3 recomputes the exponent from its sibling clue")
    down[9] = module.DOWN[9]
    down[7] = 10
    require(checks["D3"]() is False, "D3 recomputes the modulus from its sibling clue")
    down[7] = 18
    require(checks["D4"]() is False, "D4 recomputes the roots from its sibling clue")
    module = import_module("pack_grid_2023")
    across, down = dict(module.ACROSS), dict(module.DOWN)
    for answer in (0, 249, 251, 1250):
        down[7] = answer
        require(module.checks(across, down)["D7"]() is False,
                "D7 rejects a wrong point value independently of the mark lattice")


def check_all(rows=None):
    rows = rows or problem_catalog.load_records()
    targets = {ident for source in pack_grid.SOURCES.values() for ident in (source.across_id, source.down_id)}
    selected = [row for row in rows if row["id"] in targets]
    require(len(selected) == 12, "twelve crossnumber target rows")
    require(pack_gate.PROOF_TIMEOUT == 20.0, "ordinary proof timeout is unchanged")
    require(pack_gate.reprove_rows(selected) is None, "crossnumber catalog reproof and sibling consistency")
    for row in selected:
        require(row["verify"] == "sympy" and row["kind"] == "grid", row["id"] + " promoted map")
        check_promoted(row)
    check_siblings(selected)
    check_math_is_executed()
    check_clarifications(selected)
    check_contest_readings()
    print("PASS crossnumber contract (twelve proved maps, explicit conventions, wrong answers, source mutations, siblings, marking)")


if __name__ == "__main__":
    check_all()
