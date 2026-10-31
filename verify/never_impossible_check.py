#!/usr/bin/env python3
"""Reject pack records and worked notes that call a problem impossible.

Scope is the prose fields agents set on problems/records.jsonl, plus markdown
under solutions/pack, solutions/sample, and solutions/yang. An empty note is a
finding. Policy docs are not read. A negation
earlier in the same sentence ("do not mark impossible", "not impossible",
"does not claim … impossible") is not a hit. Defer, sticky, and verify: manual
are not hits.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"
NOTE_DIRS = ("solutions/pack", "solutions/sample", "solutions/yang")
PROSE_FIELDS = frozenset({
    "notes",
    "display_note",
    "worked_solution_plain",
    "worked_solution_latex",
    "answer_plain",
    "answer_latex",
})

_CLOSED = r"closed[\s-]+forms?"
_PATTERNS = (
    re.compile(r"\bimpossible\b", re.IGNORECASE),
    re.compile(r"\bimpossibilit(?:y|ies)\b", re.IGNORECASE),
    re.compile(r"\bunprove?able\b", re.IGNORECASE),
    re.compile(r"\bunsolvable\b", re.IGNORECASE),
    re.compile(r"\binsoluble\b", re.IGNORECASE),
    re.compile(r"\bnot\s+provable\b", re.IGNORECASE),
    re.compile(
        r"\bno(?:[\s-]+(?:exact|elementary|known|simple))?[\s-]+" + _CLOSED + r"\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bnon[\s-]+" + _CLOSED + r"\b", re.IGNORECASE),
    re.compile(r"\bwithout(?:\s+an?)?\s+" + _CLOSED + r"\b", re.IGNORECASE),
    re.compile(r"\black(?:s|ing)?(?:\s+an?)?\s+" + _CLOSED + r"\b", re.IGNORECASE),
    re.compile(
        r"\b(?:do|does|did)(?:\s+not|n't)\s+have\s+(?:an?\s+)?" + _CLOSED + r"\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bnot\s+expressible\s+in\s+" + _CLOSED + r"\b", re.IGNORECASE),
    re.compile(
        r"\b(?:cannot|can't|can\s+not)\s+be\s+(?:expressed|solved|integrated)\s+in\s+"
        + _CLOSED
        + r"\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bno\s+elementary\s+antiderivatives?\b", re.IGNORECASE),
    re.compile(r"\bno\s+antiderivatives?\s+in\s+" + _CLOSED + r"\b", re.IGNORECASE),
    re.compile(
        r"\b" + _CLOSED + r"\s+(?:does|do|did)(?:\s+not|n't)\s+exist\b",
        re.IGNORECASE,
    ),
)
_NEGATION = re.compile(
    r"\bnever\b|\bnot\b|\bno\s+claims?\b|\bwithout\s+claiming\b|n't\b",
    re.IGNORECASE,
)
_IMMEDIATE_NON = re.compile(r"\bnon[\s-]*$", re.IGNORECASE)

# In-memory plants. None of these write the tree.
MUTATIONS = {
    "notes-impossible": ("record", "This problem is impossible.", "impossible"),
    "notes-no-closed-form": ("record", "It has no closed form.", "no closed form"),
    "notes-unprovable": ("record", "This row is unprovable.", "unprovable"),
    "notes-unproveable": ("record", "This row is unproveable.", "unproveable"),
    "pack-note": ("solutions/pack", "This integral is impossible.", "impossible"),
    "sample-note": ("solutions/sample", "This integral has no closed form.", "no closed form"),
}

_MUST_FLAG = (
    "This integral is impossible.",
    "no closed form",
    "no-closed-form",
    "It has no closed form.",
    "The row is unprovable.",
    "The row is unproveable.",
    "cannot be expressed in closed form",
    "can't be solved in closed form",
    "no elementary antiderivative",
    "This problem is unsolvable.",
    "The equation is insoluble.",
    "not provable",
    "lacks a closed form",
    "without a closed form",
    "does not have a closed form",
    "doesn't have a closed form",
    "a closed form does not exist",
    "non-closed-form",
    "the impossibility of a closed form",
    "The integral is impossible, so do not leave it manual.",
    "not a guess\nThis integral is impossible.",
)
_MUST_ALLOW = (
    "Do not mark impossible.",
    "not impossible",
    "isn't impossible",
    "not-impossible",
    "does not claim that an alternative exact form has been proved impossible",
    "Never describe a row as impossible.",
    "not claims that a problem is impossible or has no closed form",
    "This stopping rule does not claim that an alternative exact form has been proved impossible.",
    "Answers must be in closed form. Reject infinite sums, infinite products, etc.",
    "The closed form is pi/e.",
    "The quartic piece has an elementary antiderivative.",
    "not unprovable",
    "not unproveable",
    "verify: manual",
    "Closed form (1+cot(pi/(4n)))/(2n) has SymPy limit 2/pi.",
    "Do not mark impossible or say it has no closed form.",
    "makes no claim that such replacements have been proved impossible",
)


def _normalize(text: str) -> str:
    return (
        text.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u2011", "-")
        .replace("\u2010", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )


def _sentences(text: str) -> list[str]:
    normalized = _normalize(text)
    parts = re.split(r"[\n\r]+|(?<=[.!?])\s+", normalized)
    return [re.sub(r"\s+", " ", part).strip() for part in parts if part.strip()]


def _negated(prefix: str) -> bool:
    if _IMMEDIATE_NON.search(prefix):
        return True
    return _NEGATION.search(prefix) is not None


def claims(text: str) -> list[str]:
    """Return forbidden phrases that assert impossibility, in reading order."""
    found: list[str] = []
    seen: set[str] = set()
    for sentence in _sentences(text):
        for pattern in _PATTERNS:
            for match in pattern.finditer(sentence):
                if _negated(sentence[: match.start()]):
                    continue
                phrase = match.group(0).lower()
                phrase = re.sub(r"\s+", " ", phrase)
                if phrase in seen:
                    continue
                seen.add(phrase)
                found.append(phrase)
    return found


def _self_test() -> str | None:
    for text in _MUST_FLAG:
        if not claims(text):
            return f"missed {text!r}"
    for text in _MUST_ALLOW:
        hit = claims(text)
        if hit:
            return f"flagged {text!r} via {hit}"
    return None


def load_records(path: Path) -> list[dict]:
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"FAIL never-impossible {path.relative_to(ROOT)}:{lineno} {exc}") from exc
        if not isinstance(row, dict):
            raise SystemExit(f"FAIL never-impossible {path.relative_to(ROOT)}:{lineno} not an object")
        rows.append(row)
    return rows


def prose_fields(row: dict) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []

    def walk(obj: object, path: str) -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                child = f"{path}.{key}" if path else str(key)
                if key in PROSE_FIELDS and isinstance(value, str):
                    found.append((child, value))
                else:
                    walk(value, child)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                walk(value, f"{path}[{index}]")

    walk(row, "")
    return found


def load_notes(root: Path) -> list[tuple[str, str]]:
    found = []
    for folder in NOTE_DIRS:
        directory = root / folder
        if not directory.is_dir():
            raise SystemExit(f"FAIL never-impossible missing {folder}")
        for path in sorted(directory.rglob("*.md")):
            found.append((str(path.relative_to(root)), path.read_text(encoding="utf-8")))
    return found


def scan(rows: list[dict], notes: list[tuple[str, str]]) -> list[str]:
    findings = []
    for row in rows:
        ident = str(row.get("id") or "?")
        for field, text in prose_fields(row):
            for phrase in claims(text):
                findings.append(f"problems/records.jsonl {ident} {field}: {phrase}")
    for path, text in notes:
        if not str(text).strip():
            findings.append(f"{path}: empty note")
            continue
        for phrase in claims(text):
            findings.append(f"{path}: {phrase}")
    return findings


def plant(rows: list[dict], notes: list[tuple[str, str]], name: str) -> None:
    kind, sentence, _needle = MUTATIONS[name]
    if kind == "record":
        row = rows[0]
        row["notes"] = (row.get("notes") or "") + "\n" + sentence
        return
    for index, (path, text) in enumerate(notes):
        if path.startswith(kind + "/"):
            notes[index] = (path, text + "\n" + sentence + "\n")
            return
    raise SystemExit(f"FAIL never-impossible no note under {kind}")


def main() -> int:
    broken = _self_test()
    if broken:
        print(f"FAIL never-impossible self-test {broken}")
        return 1
    args = sys.argv[1:]
    rows = load_records(RECORDS)
    notes = load_notes(ROOT)
    if args[:1] == ["--expect-fail"]:
        if len(args) != 2 or args[1] not in MUTATIONS:
            names = ", ".join(MUTATIONS)
            print(f"usage: never_impossible_check.py --expect-fail NAME ({names})", file=sys.stderr)
            return 2
        name = args[1]
        plant(rows, notes, name)
        findings = scan(rows, notes)
        _kind, _sentence, needle = MUTATIONS[name]
        where = "problems/records.jsonl" if _kind == "record" else _kind + "/"
        caught = [item for item in findings if needle in item and where in item]
        if not caught:
            print(f"FAIL mutation {name} was accepted")
            return 1
        print(f"PASS mutation {name} ({caught[0]})")
        return 0
    if args:
        print(f"unknown args {args}", file=sys.stderr)
        return 2
    findings = scan(rows, notes)
    if findings:
        for item in findings:
            print(f"FAIL never-impossible {item}")
        return 1
    pack = sum(1 for path, _text in notes if path.startswith("solutions/pack/"))
    sample = sum(1 for path, _text in notes if path.startswith("solutions/sample/"))
    yang = sum(1 for path, _text in notes if path.startswith("solutions/yang/"))
    print(
        f"PASS never-impossible ({len(rows)} records, {pack} pack notes, "
        f"{sample} sample notes, {yang} yang notes)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
