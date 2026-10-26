"""Source-bound crossnumber maps and independent per-clue proof jobs.

A grid is neither a scalar integral nor an antiderivative. Its stored problem
is a JSON manifest of the literal clues, blank lattice, printed starts, and
source PDFs. Its answer is a nonempty map from clue numbers to integer entries.
The mark grid fixes the intended solution; the year modules independently
check its mathematical and digit conditions. Each selected clue is a separate
pack_gate job, with the same timeout as an ordinary integral certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
import json
import re


@dataclass(frozen=True)
class GridSource:
    module: str
    across_id: str
    down_id: str
    across_pdf: str
    down_pdf: str
    mark_pdf: str
    across_keys: tuple[int, ...] | None = None
    down_keys: tuple[int, ...] | None = None


SOURCES = {
    "2021": GridSource(
        "pack_grid_2021", "R2-2021-Crossnumber-Across-1", "R2-2021-Crossnumber-Down-1",
        "sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf",
        "sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf",
        "sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf"),
    "2022": GridSource(
        "pack_grid_2022", "R2-2022-Crossnumber-Across-1", "R2-2022-Crossnumber-Down-1",
        "sources/past/r2/2022/Crossnumber_R2_2022_UK_University_Integration_Bee.pdf",
        "sources/past/r2/2022/Crossnumber_R2_2022_UK_University_Integration_Bee.pdf",
        "sources/past/r2/2022/Mark_Scheme_R2_2022_UK_University_Integration_Bee_(2).pdf"),
    "2023": GridSource(
        "pack_grid_2023", "R2-2023-Crossnumber-Across-1", "R2-2023-Crossnumber-Down-1",
        "sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf",
        "sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf",
        "sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf"),
    "2024": GridSource(
        "pack_grid_2024", "R2-2024-Across-Across-1", "R2-2024-Down-Down-1",
        "sources/past/r2/2024/Crossnumber_Across_2024_R2_UK_University_Integration_Bee.pdf",
        "sources/past/r2/2024/Crossnumber_Down_2024_R2_UK_University_Integration_Bee.pdf",
        "sources/past/r2/2024/Mark_Scheme_R2_2024_UK_University_Integration_Bee.pdf"),
    "2025-SG": GridSource(
        "pack_grid_2025", "R2-2025-SG-Across-Across-3", "R2-2025-SG-Down-Down-1",
        "sources/past/r2/2025/sg/2025_R2_Crossnumber_across_SG.pdf",
        "sources/past/r2/2025/sg/2025_R2_Crossnumber_Down_SG.pdf",
        "sources/past/r2/2025/sg/2025_R2_Crossnumber_Markers_grid.pdf", (3,), (1,)),
    "2025-UK": GridSource(
        "pack_grid_2025", "R2-2025-UK-Across-Across-3", "R2-2025-UK-Down-Down-1",
        "sources/past/r2/2025/uk/2025_Crossnumber_Across_Round_2.pdf",
        "sources/past/r2/2025/uk/2025_Crossnumber_Down_Round_2.pdf",
        "sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf"),
}


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _json(text):
    return json.loads(text, object_pairs_hook=_object)


def answer_map(text: str) -> dict[int, int] | None:
    """Accept JSON maps or lists of pairs; reject scalar and lossy coercions."""
    try:
        value = _json(text)
        if isinstance(value, dict):
            if any(not re.fullmatch(r"[1-9][0-9]*", k) for k in value):
                return None
            pairs = [(int(k), v) for k, v in value.items()]
        elif isinstance(value, list):
            pairs = value
        else:
            return None
        result = {}
        for pair in pairs:
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                return None
            key, entry = pair
            if type(key) is not int or key <= 0 or key in result:
                return None
            if type(entry) is not int or entry < 0:
                return None
            result[key] = entry
        return dict(sorted(result.items())) if result else None
    except (ValueError, TypeError, RecursionError):
        return None


def answer_text(values: dict[int, int]) -> str:
    return json.dumps({str(k): v for k, v in sorted(values.items())}, separators=(",", ":"))


def answers_match(answer: str, submitted: str) -> bool:
    expected = answer_map(answer)
    return expected is not None and answer_map(submitted) == expected


def _keys(source, module, direction):
    selected = source.across_keys if direction == "across" else source.down_keys
    full = module.ACROSS if direction == "across" else module.DOWN
    return tuple(sorted(full)) if selected is None else selected


def manifest(puzzle: str, direction: str) -> dict:
    if direction not in {"across", "down"}:
        raise ValueError("unknown grid direction")
    source = SOURCES[puzzle]
    module = import_module(source.module)
    clues = getattr(module, "CLUES_SG", module.CLUES) if puzzle == "2025-SG" else module.CLUES
    if set(clues) != set(module.STARTS) or any(not isinstance(value, str) or not value for value in clues.values()):
        raise ValueError("incomplete grid clue transcript")
    return {
        "contract": "crossnumber-v1",
        "puzzle": puzzle,
        "direction": direction,
        "selection": list(_keys(source, module, direction)),
        "clues": clues,
        "lattice": [re.sub(r"[0-9]", ".", line) for line in module.GRID],
        "starts": {k: list(v) for k, v in module.STARTS.items()},
        "problem_pdf": source.across_pdf if direction == "across" else source.down_pdf,
        "mark_pdf": source.mark_pdf,
    }


def problem_text(puzzle: str, direction: str) -> str:
    return json.dumps(manifest(puzzle, direction), sort_keys=True, separators=(",", ":"))


def read_problem(text: str) -> dict | None:
    try:
        value = _json(text)
        if not isinstance(value, dict):
            return None
        expected = manifest(value["puzzle"], value["direction"])
        serialized = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
        canonical = json.dumps(expected, sort_keys=True, separators=(",", ":"), allow_nan=False)
        return expected if serialized == canonical else None
    except (ValueError, TypeError, KeyError, RecursionError):
        return None


def grid_consistent(module, across, down) -> bool:
    """Read every numbered span and crossing from the original mark lattice."""
    grid = module.GRID
    if not grid or not grid[0] or any(len(line) != len(grid[0]) for line in grid):
        return False
    if any(char not in "#0123456789" for line in grid for char in line):
        return False
    expected_labels = {f"A{k}" for k in across} | {f"D{k}" for k in down}
    if set(module.STARTS) != expected_labels:
        return False
    occupied = set()
    for label, (row, col) in module.STARTS.items():
        dr, dc = (0, 1) if label[0] == "A" else (1, 0)
        before_r, before_c = row-dr, col-dc
        if 0 <= before_r < len(grid) and 0 <= before_c < len(grid[0]) and grid[before_r][before_c] != "#":
            return False
        digits = ""
        while 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != "#":
            digits += grid[row][col]
            occupied.add((row, col))
            row, col = row+dr, col+dc
        values = across if label[0] == "A" else down
        if digits != str(values[int(label[1:])]):
            return False
    cells = {(r, c) for r, line in enumerate(grid) for c, digit in enumerate(line) if digit != "#"}
    return occupied == cells


def _prepare(problem: str, answer: str):
    description = read_problem(problem)
    values = answer_map(answer)
    if description is None or values is None or list(values) != description["selection"]:
        return None
    module = import_module(SOURCES[description["puzzle"]].module)
    across, down = dict(module.ACROSS), dict(module.DOWN)
    direction = description["direction"]
    target = across if direction == "across" else down
    target.update(values)
    if not grid_consistent(module, across, down):
        return None
    prefix = "A" if direction == "across" else "D"
    labels = tuple(f"{prefix}{key}" for key in values)
    return module, across, down, labels


def proof_jobs(problem: str, limits, answer: str, variable: str):
    if limits not in (None, []) or variable != "grid":
        return None
    prepared = _prepare(problem, answer)
    if prepared is None:
        return None
    module, across, down, labels = prepared
    checks = module.checks(across, down)
    if any(label not in checks or not callable(checks[label]) for label in labels):
        return None
    return [(label, "_grid_clue", problem, [label], answer, variable) for label in labels]


def check_clue(problem: str, answer: str, labels, variable: str) -> bool:
    if variable != "grid" or not isinstance(labels, list) or len(labels) != 1:
        return False
    prepared = _prepare(problem, answer)
    if prepared is None:
        return False
    module, across, down, selected = prepared
    label = labels[0]
    if label not in selected:
        return False
    return module.checks(across, down)[label]() is True


def latex_fields(problem: str, answer: str) -> tuple[str, str]:
    description = read_problem(problem)
    values = answer_map(answer)
    if description is None or values is None:
        raise ValueError("invalid grid fields")
    prefix = "A" if description["direction"] == "across" else "D"
    prompt = r"\text{Crossnumber clues }" + ", ".join(f"{prefix}_{{{k}}}" for k in values)
    result = r"\begin{array}{r|r}\text{clue}&\text{entry}\\" + r"\\".join(f"{k}&{v}" for k, v in values.items()) + r"\end{array}"
    return prompt, result


def prompt_text(description: dict) -> str:
    prefix = "A" if description["direction"] == "across" else "D"
    return "\n".join(f"{prefix}{key}. {description['clues'][f'{prefix}{key}']}" for key in description["selection"])


def row_problem(row: dict) -> str | None:
    if row.get("kind") != "grid" or row.get("variable") != "grid" or row.get("limits") != []:
        return "grid shape"
    description = read_problem(row.get("sympy_expr", ""))
    if description is None or _prepare(row["sympy_expr"], row.get("answer_sympy", "")) is None:
        return "grid source or answer mismatch"
    source = SOURCES[description["puzzle"]]
    expected_id = source.across_id if description["direction"] == "across" else source.down_id
    if row.get("id") != expected_id:
        return "grid row and source direction differ"
    year, _, region = description["puzzle"].partition("-")
    problem_id = ("Across" if description["direction"] == "across" else "Down") + f"-{description['selection'][0]}"
    if (row.get("year") != year or row.get("region") != (region.lower() or None)
            or row.get("round") != "r2" or row.get("pdf_role") != "problems"
            or row.get("problem_id") != problem_id):
        return "grid catalog metadata drift"
    if row.get("pdf_path") != description["problem_pdf"] or row.get("answer_source_pdf") != description["mark_pdf"]:
        return "grid source citation mismatch"
    if row.get("integrand_plain") != prompt_text(description):
        return "grid plain clue transcript drift"
    printed = _printed_map({"answer_plain": row.get("answer_plain")}, description["selection"])
    if printed != answer_map(row.get("answer_sympy", "")):
        return "grid printed answer drift"
    prompt, answer = latex_fields(row["sympy_expr"], row["answer_sympy"])
    if row.get("integrand_latex") != prompt or row.get("answer_latex") != answer:
        return "grid latex drift"
    if row.get("worked_solution_latex") is not None:
        return "invented worked latex"
    return None


def _printed_map(row, keys):
    if row.get("kind") == "grid" and row.get("verify") == "sympy":
        return answer_map(row.get("answer_sympy", ""))
    text = str(row.get("answer_plain") or "").strip()
    if len(keys) == 1 and re.fullmatch(r"[0-9]+", text):
        return {keys[0]: int(text)}
    pairs = text.split(";")
    values = {}
    for pair in pairs:
        match = re.fullmatch(r"\s*([1-9][0-9]*)\s+([0-9]+)\s*", pair)
        if match is None or int(match[1]) in values:
            return None
        values[int(match[1])] = int(match[2])
    return values


def sibling_problem(rows: list[dict]) -> str | None:
    """Check any supplied sibling catalog rows, including manual siblings."""
    by_id = {row.get("id"): row for row in rows}
    for row in rows:
        if row.get("verify") != "sympy" or row.get("kind") != "grid":
            continue
        description = read_problem(row.get("sympy_expr", ""))
        if description is None:
            return f"{row.get('id')} invalid grid manifest"
        source = SOURCES[description["puzzle"]]
        module = import_module(source.module)
        across, down = dict(module.ACROSS), dict(module.DOWN)
        for direction, ident, values in (("across", source.across_id, across), ("down", source.down_id, down)):
            sibling = by_id.get(ident)
            if sibling is None:
                continue
            keys = _keys(source, module, direction)
            reading = _printed_map(sibling, keys)
            if reading is None or tuple(sorted(reading)) != keys:
                return f"{ident} grid clue keys differ"
            values.update(reading)
        if not grid_consistent(module, across, down):
            return f"{row.get('id')} sibling grid digits disagree"
    return None
