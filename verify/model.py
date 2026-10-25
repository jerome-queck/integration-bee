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


SESSION_PHASES = {
    "idle",
    "awaiting_answer",
    "mock_open",
    "mock_awaiting",
    "aptitude",
    "proposing",
}

POLICY_DETAILS = {"worked", "faded", "bare"}
POLICY_KINDS = {"definite", "indefinite", "any"}


def _id_list(value, label: str) -> str | None:
    if not isinstance(value, list):
        return f"aptitude {label} must be a list"
    seen = set()
    for item in value:
        if not isinstance(item, str) or item == "" or item in seen:
            return f"aptitude {label} needs unique ids"
        seen.add(item)
    return None


def aptitude_problem(value) -> str | None:
    if not isinstance(value, dict):
        return "aptitude needs full_coverage, offer, and declined"
    if set(value) != {"full_coverage", "offer", "declined"}:
        return "aptitude needs full_coverage, offer, and declined"
    if not isinstance(value.get("full_coverage"), bool):
        return "aptitude full_coverage must be bool"
    err = _id_list(value.get("offer"), "offer")
    if err:
        return err
    return _id_list(value.get("declined"), "declined")


def policy_problem(value) -> str | None:
    if not isinstance(value, dict):
        return "policy needs rows"
    allowed = {"approach", "detail", "kind", "volume"}
    for row in value.values():
        if not isinstance(row, dict) or set(row) != allowed:
            return "policy row needs approach, detail, kind, and volume"
        approach = row.get("approach")
        if not isinstance(approach, str) or approach == "":
            return "policy approach is empty"
        if row.get("detail") not in POLICY_DETAILS:
            return "policy detail is bad"
        if row.get("kind") not in POLICY_KINDS:
            return "policy kind is bad"
        volume = row.get("volume")
        if isinstance(volume, bool) or not isinstance(volume, int) or volume < 0:
            return "policy volume is bad"
    return None


def coach_queue_done(status: str | None, full_coverage: bool) -> bool:
    """True when the coach queue leaves this node.

    solid is done. skipped is done unless full_coverage is on.
    learning and a missing tick stay in the queue.
    mock_block_reason does not call this.
    """
    if status == "solid":
        return True
    if status == "skipped" and not full_coverage:
        return True
    return False


def session_problem(doc: dict) -> str | None:
    phase = doc.get("phase")
    if phase not in SESSION_PHASES:
        return "bad session phase"
    problem = doc.get("problem_id")
    mock = doc.get("mock_id")
    node = doc.get("node")
    if phase == "idle" and (problem or mock or node):
        return "idle session still open"
    if phase == "awaiting_answer" and (not problem or not node or mock):
        return "awaiting session needs a node and a problem"
    if phase == "mock_open" and (not mock or problem):
        return "mock session needs a mock id"
    if phase == "mock_awaiting" and (not mock or not problem):
        return "mock question needs a mock and a problem"
    if phase == "aptitude" and (not problem or mock):
        return "aptitude session needs a problem"
    if phase == "proposing" and (problem or mock or node):
        return "proposing session is waiting for confirm"
    err = aptitude_problem(doc.get("aptitude")) if "aptitude" in doc else None
    if err:
        return err
    if phase == "proposing" and not (doc.get("aptitude") or {}).get("offer"):
        return "proposing session needs an offer"
    if "policy" in doc:
        return policy_problem(doc.get("policy"))
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


STICKY_FULL = 5


def mark_problem(marks: dict) -> str | None:
    for mark_id, row in marks.items():
        if not mark_id:
            return "mark needs an id"
        if not isinstance(row, dict):
            return "mark needs answer_ok and method_ok"
        if "correct" in row:
            return "mark has correct"
        answer_ok = row.get("answer_ok")
        method_ok = row.get("method_ok")
        if not isinstance(answer_ok, bool) or not isinstance(method_ok, bool):
            return "mark needs answer_ok and method_ok"
        technique = row.get("technique")
        if not isinstance(technique, str) or not technique:
            return "mark needs technique"
        if "note" in row:
            note = row["note"]
            if not isinstance(note, str) or not note:
                return "mark needs a note"
    return None


def put_mark(marks: dict, mark_id: str, *, answer_ok: bool, method_ok: bool, technique: str, note: str = "") -> dict:
    out = {key: dict(row) for key, row in marks.items()}
    row = {"answer_ok": answer_ok, "method_ok": method_ok, "technique": technique}
    if note:
        row["note"] = note
    out[mark_id] = row
    return out


def sticky_problem(cards: dict) -> str | None:
    for technique, card in cards.items():
        if not technique:
            return "sticky needs a technique"
        if not isinstance(card, dict):
            return "sticky needs a note"
        note = card.get("note")
        if not isinstance(note, str) or not note:
            return "sticky needs a note"
        touched = card.get("touched")
        if not isinstance(touched, str) or not ISO_DAY.match(touched):
            return "bad sticky day"
        if "strength" in card:
            return "sticky strength is derived"
    return None


def put_sticky(cards: dict, technique: str, note: str, today: date) -> dict:
    out = {key: dict(card) for key, card in cards.items()}
    out[technique] = {"note": note, "touched": today.isoformat()}
    return out


def sticky_strength(touched: str, today: date) -> int:
    start = date.fromisoformat(touched)
    if start > today:
        return STICKY_FULL
    return max(0, STICKY_FULL - (today - start).days)
