#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import sympy as sp

import check_math

ROOT = Path(__file__).resolve().parent.parent
INDEX_REL = Path("docs/techniques/beyond-yang.md")
SKILL = Path(".cursor/skills/integration-bee-companion/SKILL.md")
SESSION_SENTENCE = "A study session does not edit a teaching note."
FORBIDDEN_PHRASE = "add the move there"
FORBIDDEN_IDS = ("R1-", "R2-", "R3-", "YANG-")

NS = {
    "x": sp.symbols("x", real=True),
    "log": sp.log,
    "exp": sp.exp,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "sqrt": sp.sqrt,
    "pi": sp.pi,
    "Piecewise": sp.Piecewise,
    "True": True,
}


class Repeat(Enum):
    SAME = "same"
    FILL = "fill"
    REJECT = "reject"


@dataclass(frozen=True)
class Gap:
    id: str
    note: str
    cite: str
    catalog: str | None
    contains: tuple[str, ...]
    examples: int


@dataclass(frozen=True)
class Index:
    gaps: tuple[Gap, ...]

    def by_id(self, gap_id: str) -> Gap | None:
        for gap in self.gaps:
            if gap.id == gap_id:
                return gap
        return None


def load_index(root: Path | None = None) -> tuple[Index | None, str | None]:
    root = root or ROOT
    path = root / INDEX_REL
    try:
        text = path.read_text()
    except OSError:
        return None, "gap index is unreadable"
    gaps, err = _parse(text)
    if err:
        return None, "gap index is unreadable"
    return Index(tuple(gaps)), None


def parse_gap(raw: object, index: Index) -> tuple[Gap | None, str | None]:
    if not isinstance(raw, str) or not raw.strip():
        return None, "unknown gap"
    gap = index.by_id(raw.strip())
    if gap is None:
        return None, "unknown gap"
    return gap, None


def note_say(unit: str | None, gap: Gap | None, correct: bool) -> str:
    if correct and gap is None:
        return "The final answer matches."
    if correct and gap is not None:
        return f"The final answer matches. Teach the method gap from {gap.note}."
    if gap is not None:
        return f"The final answer does not match. Teach the gap from {gap.note}."
    if unit:
        return f"The final answer does not match. Teach the gap from units/{unit}/teaching.tex."
    return "The final answer does not match."


def classify_repeat(stored: str | None, incoming: str | None) -> Repeat:
    if incoming is None or incoming == stored:
        return Repeat.SAME
    if stored is None:
        return Repeat.FILL
    return Repeat.REJECT


def check_index(root: Path, catalog: list[dict], extra: list[str] | None = None) -> list[str]:
    index, err = load_index(root)
    if err or index is None:
        return [err or "gap index is unreadable"]
    errors: list[str] = []
    errors.extend(_order_errors(index))
    errors.extend(_catalog_errors(index, catalog))
    errors.extend(_file_errors(root, index, extra or []))
    errors.extend(_note_errors(root, index))
    errors.extend(_skill_errors(root))
    return errors


def _parse(text: str) -> tuple[list[Gap], str | None]:
    gaps: list[Gap] = []
    current: dict | None = None
    seen: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            if current is not None:
                gap, err = _finish(current)
                if err:
                    return [], err
                if gap.id in seen:
                    return [], "duplicate"
                seen.add(gap.id)
                gaps.append(gap)
            current = {"id": line[3:].strip()}
            continue
        if current is None or not line.startswith("- "):
            continue
        body = line[2:]
        if ":" not in body:
            return [], "field"
        key, value = body.split(":", 1)
        current[key.strip()] = value.strip()
    if current is not None:
        gap, err = _finish(current)
        if err:
            return [], err
        if gap.id in seen:
            return [], "duplicate"
        gaps.append(gap)
    if len(gaps) != 6:
        return [], "count"
    return gaps, None


def _finish(fields: dict) -> tuple[Gap, str | None]:
    try:
        catalog = fields.get("catalog") or None
        contains = tuple(part.strip() for part in fields["contains"].split(",") if part.strip())
        gap = Gap(
            id=fields["id"],
            note=fields["note"],
            cite=fields["cite"],
            catalog=catalog,
            contains=contains,
            examples=int(fields["examples"]),
        )
    except (KeyError, ValueError):
        return Gap("", "", "", None, (), 0), "fields"
    if not gap.id or not gap.note or not gap.cite or not gap.contains:
        return gap, "fields"
    return gap, None


def _section_key(cite: str) -> tuple[int, int]:
    match = re.search(r"section\s+(\d+)\.(\d+)", cite)
    if not match:
        return (10**6, 10**6)
    return (int(match.group(1)), int(match.group(2)))


def _order_errors(index: Index) -> list[str]:
    keys = [_section_key(gap.cite) for gap in index.gaps]
    if keys != sorted(keys):
        return ["gap headings are out of guide order"]
    if keys[-1] != (10**6, 10**6):
        return ["the format row must be last"]
    if keys.count((10**6, 10**6)) != 1:
        return ["more than one row has no section number"]
    return []


def _catalog_errors(index: Index, catalog: list[dict]) -> list[str]:
    nodes = {node["id"]: node for node in catalog}
    errors = []
    for gap in index.gaps:
        if not gap.catalog:
            if gap.id in nodes:
                errors.append(f"{gap.id} is a catalog id with an empty catalog field")
            continue
        node = nodes.get(gap.catalog)
        if node is None:
            errors.append(f"{gap.id} names a missing catalog id {gap.catalog}")
            continue
        unit = node.get("unit")
        if node.get("status") == "deferred" or not unit:
            if unit:
                errors.append(f"{gap.catalog} is deferred and still has a unit")
            if not gap.note.endswith(".md"):
                errors.append(f"{gap.id} deferred note is not markdown")
            continue
        expected = f"units/{unit}/teaching.tex"
        if gap.note != expected:
            errors.append(f"{gap.id} note is {gap.note}, catalog unit wants {expected}")
    return errors


def _file_errors(root: Path, index: Index, extra: list[str]) -> list[str]:
    allowed = {INDEX_REL.as_posix()}
    for gap in index.gaps:
        if gap.note.startswith("docs/techniques/"):
            allowed.add(gap.note)
    folder = root / "docs" / "techniques"
    found = {path.relative_to(root).as_posix() for path in folder.iterdir() if path.is_file()}
    found.update(extra)
    extra_found = sorted(found - allowed)
    missing = sorted(allowed - found)
    errors = []
    if extra_found:
        errors.append("docs/techniques has extra files: " + ", ".join(extra_found))
    if missing:
        errors.append("docs/techniques is missing: " + ", ".join(missing))
    return errors


def _fences(text: str) -> list[dict[str, str]]:
    blocks = re.findall(r"```ib-example\n(.*?)```", text, re.S)
    parsed = []
    for block in blocks:
        fields = {}
        for line in block.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        parsed.append(fields)
    return parsed


def _fence_ok(fields: dict[str, str]) -> str | None:
    for key in ("integrand", "answer"):
        if key not in fields:
            return "fence missing integrand or answer"
    if any(token in " ".join(fields.values()) for token in FORBIDDEN_IDS):
        return "fence names a catalog id"
    if "verify: manual" in " ".join(fields.values()):
        return "fence claims a manual answer"
    try:
        integrand = sp.sympify(fields["integrand"], locals=NS)
        answer = sp.sympify(fields["answer"], locals=NS)
    except Exception as exc:
        return f"fence did not parse: {exc}"
    if "limits" not in fields:
        if check_math.is_antiderivative(answer, integrand):
            return None
        return "indefinite fence is not an antiderivative"
    try:
        lo_s, hi_s = [part.strip() for part in fields["limits"].split(",", 1)]
        lo = sp.sympify(lo_s, locals=NS)
        hi = sp.sympify(hi_s, locals=NS)
        got = sp.simplify(sp.integrate(integrand, (NS["x"], lo, hi)) - answer)
    except Exception as exc:
        return f"definite fence failed: {exc}"
    if got == 0:
        return None
    return f"definite fence disagrees: {got}"


def _note_errors(root: Path, index: Index) -> list[str]:
    errors = []
    for gap in index.gaps:
        path = root / gap.note
        if not path.is_file():
            errors.append(f"missing note {gap.note}")
            continue
        text = path.read_text()
        for token in gap.contains:
            if token not in text:
                errors.append(f"{gap.note} missing {token}")
        for forbidden in FORBIDDEN_IDS:
            if forbidden in text:
                errors.append(f"{gap.note} contains {forbidden}")
        fences = _fences(text)
        if len(fences) != gap.examples:
            errors.append(f"{gap.note} has {len(fences)} fences, wants {gap.examples}")
        for fields in fences:
            err = _fence_ok(fields)
            if err:
                errors.append(f"{gap.note} {err}")
    return errors


def _skill_errors(root: Path) -> list[str]:
    text = (root / SKILL).read_text()
    errors = []
    if SESSION_SENTENCE not in text:
        errors.append("companion skill is missing the session sentence")
    if FORBIDDEN_PHRASE in text:
        errors.append("companion skill still tells the session to edit the note")
    return errors


def main() -> int:
    args = sys.argv[1:]
    catalog = __import__("json").loads((ROOT / "trackers" / "catalog.json").read_text())["nodes"]
    if args[:1] == ["--expect-fail"]:
        if args[1:] != ["extra-file"]:
            print("usage: gap_index.py --expect-fail extra-file", file=sys.stderr)
            return 2
        errors = check_index(ROOT, catalog, extra=["docs/techniques/extra.md"])
        if not any("extra" in err for err in errors):
            print("FAIL expected extra-file")
            return 1
        print("PASS mutation extra-file")
        return 0
    if args:
        print(f"unknown args {args}", file=sys.stderr)
        return 2
    errors = check_index(ROOT, catalog)
    if errors:
        for err in errors:
            print(f"FAIL gap index {err}")
        return 1
    print("PASS gap index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
