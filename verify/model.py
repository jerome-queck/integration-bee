"""Predicates for unit order, Round 1 readiness, and tracker records."""

from __future__ import annotations

import re
from datetime import date

ISO_DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TICK_STATUS = {"learning", "solid", "skipped"}


def classify_meta(text: str) -> str:
    if re.search(r"past_paper:\s*true", text):
        return "past"
    if re.search(r"kind:\s*concept", text) or re.search(r"past_paper:\s*false", text):
        return "concept"
    return "other"


def concept_gap(past: list[str], concept: list[str]) -> bool:
    return bool(past) and not concept


def unit01_problem(text: str) -> str | None:
    if re.search(r"past_paper:\s*true", text):
        return "unit 01 marked past_paper"
    if "yang:1.1" not in text or "yang:1.2" not in text:
        return "unit 01 missing yang:1.1 or yang:1.2"
    return None


def mock_block_reason(ticks: dict, round1_ids: list[str], cold: bool) -> str | None:
    if cold:
        return None
    missing = []
    for node in round1_ids:
        row = ticks.get(node) or {}
        status = row.get("status") if isinstance(row, dict) else row
        if status != "solid":
            missing.append(node)
    if missing:
        return "round1 nodes not solid: " + ",".join(missing)
    return None


def tick_problem(ticks: dict, catalog_ids: set[str]) -> str | None:
    for node, row in ticks.items():
        if node not in catalog_ids:
            return f"unknown node {node}"
        status = row.get("status") if isinstance(row, dict) else row
        if status not in TICK_STATUS:
            return f"bad status {status}"
    return None


def attempt_problem(item: dict) -> str | None:
    if not item.get("problem_id"):
        return "attempt missing problem_id"
    interval = item.get("interval_days", 0)
    if not isinstance(interval, int) or isinstance(interval, bool) or interval < 0:
        return "negative interval"
    due = item.get("next_due")
    if due is not None and not ISO_DAY.match(str(due)):
        return "bad next_due"
    return None


def heatmap_problem(topics: dict) -> str | None:
    for name, row in topics.items():
        attempts = row.get("attempts", 0)
        fails = row.get("fails", 0)
        if attempts < 0 or fails < 0:
            return f"negative count {name}"
        if fails > attempts:
            return f"fails exceed attempts {name}"
    return None


def streak_problem(days: list) -> str | None:
    seen = set()
    for day in days:
        if not ISO_DAY.match(str(day)):
            return f"bad day {day}"
        if day in seen:
            return f"duplicate day {day}"
        seen.add(day)
    return None


def journal_problem(note: dict) -> str | None:
    if not note.get("technique") or not note.get("note"):
        return "journal note needs technique and note"
    return None


def mock_session_problem(session: dict) -> str | None:
    if not session.get("id"):
        return "mock missing id"
    score = session.get("score")
    out_of = session.get("out_of")
    if score is not None and out_of is not None and (score < 0 or score > out_of):
        return "mock score out of range"
    return None


def next_srs(prev: dict | None, correct: bool, today: date) -> dict:
    ease = float((prev or {}).get("ease", 2.5))
    reps = int((prev or {}).get("reps", 0))
    interval = int((prev or {}).get("interval_days", 0))
    if correct:
        reps += 1
        if reps == 1:
            interval = 1
        elif reps == 2:
            interval = 3
        else:
            interval = max(1, round(interval * ease))
    else:
        reps = 0
        interval = 1
        ease = max(1.3, ease - 0.2)
    due = date.fromordinal(today.toordinal() + interval)
    return {
        "ease": round(ease, 2),
        "reps": reps,
        "interval_days": interval,
        "next_due": due.isoformat(),
    }


def due_ids(items: list[dict], today: date) -> list[str]:
    latest: dict[str, dict] = {}
    for item in items:
        pid = item.get("problem_id")
        if pid:
            latest[pid] = item
    today_iso = today.isoformat()
    return [
        pid
        for pid, item in latest.items()
        if item.get("next_due") and item["next_due"] <= today_iso
    ]


def bump_heatmap(topics: dict, tags: list[str], correct: bool) -> dict:
    out = {key: dict(row) for key, row in topics.items()}
    for tag in tags:
        row = out.setdefault(tag, {"attempts": 0, "fails": 0})
        row["attempts"] = int(row.get("attempts", 0)) + 1
        if not correct:
            row["fails"] = int(row.get("fails", 0)) + 1
    return out


def touch_streak(days: list[str], today: date) -> dict:
    seen = set(days)
    seen.add(today.isoformat())
    ordered = sorted(seen)
    current = 0
    cursor = today
    while cursor.isoformat() in seen:
        current += 1
        cursor = date.fromordinal(cursor.toordinal() - 1)
    best = 0
    run = 0
    prev = None
    for iso in ordered:
        cur = date.fromisoformat(iso)
        if prev is not None and cur.toordinal() == prev.toordinal() + 1:
            run += 1
        else:
            run = 1
        best = max(best, run)
        prev = cur
    return {"days": ordered, "current": current, "best": best}
