from __future__ import annotations

import check_math
import model
import sympy as sp
import yaml

PHASE_IDLE = "idle"
PHASE_AWAITING = "awaiting_answer"
PHASE_MOCK = "mock_open"
PHASE_MOCK_Q = "mock_awaiting"


def empty_session() -> dict:
    return {
        "schema": "integration-bee-session/v1",
        "phase": PHASE_IDLE,
        "node": None,
        "problem_id": None,
        "mock_id": None,
        "updated": None,
    }


def yang_tag(node: dict) -> str | None:
    yang = node.get("yang")
    if not yang:
        return None
    text = str(yang)
    if text.startswith("yang:"):
        return text
    return f"yang:{text}"


def _status(ticks: dict, node_id: str) -> str | None:
    row = ticks.get(node_id) or {}
    if isinstance(row, dict):
        return row.get("status")
    return row


def _solid(ticks: dict, node_id: str) -> bool:
    return _status(ticks, node_id) == "solid"


def teachable(catalog: list[dict]) -> list[dict]:
    return [node for node in catalog if node.get("unit") and node.get("status") == "ready"]


def node_tags(node: dict, drills: list[dict]) -> set[str]:
    tag = yang_tag(node)
    tags: set[str] = set()
    if tag:
        tags.add(tag)
    for drill in drills:
        if drill.get("unit") != node.get("unit"):
            continue
        bag = set(drill.get("yang") or [])
        bag.update(drill.get("technique_tags") or [])
        if tag and tag not in bag:
            continue
        if drill.get("technique"):
            tags.add(drill["technique"])
        tags.update(drill.get("technique_tags") or [])
        tags.update(drill.get("yang") or [])
    return tags


def weak_topics(heat: dict) -> list[dict]:
    topics = heat.get("topics") or {}
    rows = [
        {"tag": tag, "attempts": row.get("attempts", 0), "fails": row.get("fails", 0)}
        for tag, row in topics.items()
        if row.get("fails", 0) > 0
    ]
    return sorted(rows, key=lambda row: (-row["fails"], row["tag"]))


def recommend_node(catalog: list[dict], ticks: dict, heat: dict, drills: list[dict]) -> dict | None:
    nodes = teachable(catalog)
    tagged = [(node, node_tags(node, drills)) for node in nodes]
    for topic in weak_topics(heat):
        for node, tags in tagged:
            if topic["tag"] in tags and not _solid(ticks, node["id"]):
                return node
    for node, _tags in tagged:
        if not _solid(ticks, node["id"]):
            return node
    return None


def readiness(catalog: list[dict], ticks: dict) -> dict:
    missing = [
        node["id"]
        for node in catalog
        if node.get("gate") == "round1" and not _solid(ticks, node["id"])
    ]
    return {"ready": not missing, "missing_round1": missing}


def drill_public(row: dict) -> dict:
    return {
        "id": row["id"],
        "unit": row["unit"],
        "technique": row.get("technique"),
        "latex": row.get("latex"),
        "kind": row.get("kind"),
        "yang": row.get("yang") or [],
        "hint": row.get("hint") or "",
        "teaching": f"units/{row['unit']}/teaching.tex",
    }


def candidates_for(node: dict, drills: list[dict]) -> list[dict]:
    tag = yang_tag(node)
    rows = []
    for drill in drills:
        if drill.get("unit") != node.get("unit"):
            continue
        bag = set(drill.get("yang") or [])
        bag.update(drill.get("technique_tags") or [])
        if tag and tag not in bag:
            continue
        rows.append(drill)
    return rows


def pick_drill(node: dict, drills: list[dict], attempts: list[dict]) -> dict | None:
    rows = candidates_for(node, drills)
    if not rows:
        return None
    correct = {item.get("problem_id") for item in attempts if item.get("correct") is True}
    last_wrong = None
    for item in attempts:
        if item.get("correct") is False:
            last_wrong = item.get("problem_id")
    fresh = [row for row in rows if row["id"] not in correct and row["id"] != last_wrong]
    if fresh:
        return fresh[0]
    unseen = [row for row in rows if row["id"] not in correct]
    if unseen:
        return unseen[0]
    return rows[0]


def find_drill(drills: list[dict], drill_id: str) -> dict | None:
    for row in drills:
        if row["id"] == drill_id:
            return row
    return None


def coach_view(catalog: list[dict], ticks: dict, heat: dict, drills: list[dict]) -> dict:
    node = recommend_node(catalog, ticks, heat, drills)
    gate = readiness(catalog, ticks)
    return {
        "next_node": node["id"] if node else None,
        "unit": node.get("unit") if node else None,
        "teaching": f"units/{node['unit']}/teaching.tex" if node else None,
        "ready": gate["ready"],
        "missing_round1": gate["missing_round1"],
        "weak": weak_topics(heat),
    }


def _mark_namespace():
    ns = dict(check_math.NS)
    ns["ln"] = ns["log"]
    ns["C"] = sp.symbols("C")
    return ns


def parse_expr(text: str):
    return sp.sympify(text, locals=_mark_namespace())


def _drop_abs(expr):
    return expr.replace(sp.Abs, lambda arg: arg)


def expressions_match(answer: str, submitted: str, indefinite: bool) -> bool:
    ns = _mark_namespace()
    ans = sp.sympify(answer, locals=ns)
    got = sp.sympify(submitted, locals=ns)
    if sp.simplify(got - ans) == 0:
        return True
    if not indefinite:
        return False
    ans = _drop_abs(ans)
    got = _drop_abs(got)
    if sp.simplify(got - ans) == 0:
        return True
    return sp.simplify(sp.diff(got - ans, ns["x"])) == 0


def _indefinite(row: dict) -> bool:
    if row.get("kind") == "indefinite":
        return True
    limits = row.get("limits")
    return limits in (None, [])


def grade_problem(
    problem_id: str,
    submitted: str,
    verdict: str | None,
    drills: list[dict],
    feed: list[dict],
    catalog_rows: list[dict] | None = None,
):
    drill = find_drill(drills, problem_id)
    if drill is not None:
        try:
            correct = expressions_match(drill["answer_sympy"], submitted, _indefinite(drill))
        except Exception as exc:
            return None, f"answer did not parse: {exc}"
        tags = list(drill.get("technique_tags") or [])
        display = drill.get("answer_display")
        return {"correct": correct, "tags": tags, "display": display, "row": drill, "manual": False}, None
    feed_row = next((row for row in feed if row.get("id") == problem_id), None)
    if feed_row is None:
        catalog_row = next((row for row in (catalog_rows or []) if row.get("id") == problem_id), None)
        if catalog_row is None:
            return None, f"unknown problem {problem_id}"
        if catalog_row.get("answer_sympy") or catalog_row.get("integrand_latex"):
            return None, "catalog problem is not sympy-checked"
        if catalog_row.get("verify") != "manual" or not catalog_row.get("answer_plain"):
            return None, "unchecked catalog problem has no printed answer"
        if verdict not in {"correct", "incorrect"}:
            return None, "manual problem needs verdict"
        tags = list(catalog_row.get("technique_tags") or [])
        tags.extend(catalog_row.get("yang") or [])
        return {
            "correct": verdict == "correct",
            "tags": tags,
            "display": catalog_row.get("answer_plain"),
            "row": {"id": problem_id},
            "manual": True,
        }, None
    tags = list(feed_row.get("technique_tags") or [])
    if feed_row.get("answer_sympy"):
        try:
            correct = expressions_match(feed_row["answer_sympy"], submitted, _indefinite(feed_row))
        except Exception as exc:
            return None, f"answer did not parse: {exc}"
        display = feed_row.get("answer_display_correct") or feed_row.get("answer_display")
        return {"correct": correct, "tags": tags, "display": display, "row": feed_row, "manual": False}, None
    if verdict not in {"correct", "incorrect"}:
        return None, "manual problem needs verdict"
    return {
        "correct": verdict == "correct",
        "tags": tags,
        "display": feed_row.get("answer_display"),
        "row": feed_row,
        "manual": True,
    }, None


def _latest(attempts: list[dict], problem_id: str) -> dict | None:
    found = None
    for item in attempts:
        if item.get("problem_id") == problem_id:
            found = item
    return found


def _set_phase(session: dict, phase: str, node, problem_id, mock_id, updated: str) -> dict:
    doc = {
        "schema": "integration-bee-session/v1",
        "phase": phase,
        "node": node,
        "problem_id": problem_id,
        "mock_id": mock_id,
        "updated": updated,
    }
    err = model.session_problem(doc)
    if err:
        raise ValueError(err)
    return doc


def _clear_to(session: dict, updated: str) -> dict:
    if session.get("mock_id") and session.get("phase") in {PHASE_MOCK, PHASE_MOCK_Q}:
        return _set_phase(session, PHASE_MOCK, None, None, session["mock_id"], updated)
    return _set_phase(session, PHASE_IDLE, None, None, None, updated)


def distinct_correct(node: dict, drills: list[dict], attempts: list[dict]) -> int:
    ids = {row["id"] for row in candidates_for(node, drills)}
    got = set()
    for item in attempts:
        if item.get("correct") is True and item.get("problem_id") in ids:
            got.add(item["problem_id"])
    return len(got)


def plan_teach(session, attempts, ticks, catalog, drills, heat, updated: str) -> dict:
    phase = session.get("phase") or PHASE_IDLE
    if phase in {PHASE_AWAITING, PHASE_MOCK_Q} and session.get("problem_id"):
        drill = find_drill(drills, session["problem_id"])
        view = drill_public(drill) if drill else {"id": session["problem_id"]}
        return {
            "exit": 0,
            "error": None,
            "session": session,
            "effects": {},
            "drill": view,
            "say": "The same integral is still open. Show it again. Do not show an answer.",
            "mark": None,
            "tick": None,
        }
    if phase == PHASE_MOCK:
        return {
            "exit": 2,
            "error": "a mock is open",
            "session": session,
            "effects": {},
            "drill": None,
            "say": "Finish or mark the open mock before teaching a new node.",
            "mark": None,
            "tick": None,
        }
    node = recommend_node(catalog, ticks, heat, drills)
    if node is None:
        return {
            "exit": 0,
            "error": None,
            "session": session,
            "effects": {},
            "drill": None,
            "say": "Every teachable node is solid. Offer a mock or a due review.",
            "mark": None,
            "tick": None,
        }
    drill = pick_drill(node, drills, attempts)
    if drill is None:
        return {
            "exit": 2,
            "error": f"no drill for {node['id']}",
            "session": session,
            "effects": {},
            "drill": None,
            "say": "",
            "mark": None,
            "tick": None,
        }
    new_session = _set_phase(session, PHASE_AWAITING, node["id"], drill["id"], None, updated)
    tick = None
    if _status(ticks, node["id"]) is None:
        tick = {"node": node["id"], "status": "learning"}
    return {
        "exit": 0,
        "error": None,
        "session": new_session,
        "effects": {},
        "drill": drill_public(drill),
        "say": f"Teach {node['id']} from units/{node['unit']}/teaching.tex. Then set this integral.",
        "mark": None,
        "tick": tick,
    }


def gap_rows(graded: dict, problem_id: str, method_note: str) -> tuple[dict | None, dict | None]:
    if not graded["correct"]:
        return None, None
    technique = graded["tags"][0] if graded["tags"] else problem_id
    if method_note:
        return (
            {
                "id": problem_id,
                "answer_ok": True,
                "method_ok": False,
                "technique": technique,
                "note": method_note,
            },
            {"technique": technique, "note": method_note},
        )
    return (
        {
            "id": problem_id,
            "answer_ok": True,
            "method_ok": True,
            "technique": technique,
        },
        None,
    )


def plan_mark(
    session,
    attempts,
    ticks,
    catalog,
    drills,
    feed,
    body: dict,
    updated: str,
    catalog_rows: list[dict] | None = None,
) -> dict:
    problem_id = body.get("problem_id")
    source = body.get("source")
    extract = body.get("extract") or {}
    submitted = extract.get("final_answer")
    verdict = body.get("verdict")
    method_note = (extract.get("method_note") or "").strip()
    if source not in {"photo", "typed"}:
        return _fail(session, 2, "mark needs source photo or typed")
    if not problem_id or submitted is None or str(submitted).strip() == "":
        return _fail(session, 2, "mark needs problem_id and extract.final_answer")
    submitted = str(submitted).strip()
    graded, err = grade_problem(problem_id, submitted, verdict, drills, feed, catalog_rows)
    if err:
        return _fail(session, 2, err)
    latest = _latest(attempts, problem_id)
    open_match = session.get("problem_id") == problem_id and session.get("phase") in {PHASE_AWAITING, PHASE_MOCK_Q}
    if (
        open_match
        and latest
        and latest.get("submitted") == submitted
        and latest.get("correct") is graded["correct"]
    ):
        new_session = _clear_to(session, updated)
        tick = None
        if graded["correct"]:
            node = _node_for_problem(problem_id, catalog, drills, session)
            if node is not None and distinct_correct(node, drills, attempts) >= 2 and not _solid(ticks, node["id"]):
                tick = {"node": node["id"], "status": "solid"}
        ledger, sticky = gap_rows(graded, problem_id, method_note) if method_note else (None, None)
        return {
            "exit": 0 if graded["correct"] else 1,
            "error": None,
            "session": new_session,
            "effects": {},
            "drill": None,
            "say": "That mark was already recorded.",
            "mark": {
                "id": problem_id,
                "correct": graded["correct"],
                "idempotent": True,
                "expected_display": graded["display"],
                "source": source,
            },
            "tick": tick,
            "journal": None,
            "ledger": ledger,
            "sticky": sticky,
        }
    note = "final answer matched" if graded["correct"] else "final answer differed"
    if graded["manual"]:
        note = "manual mark"
    journal = None
    if graded["correct"] and method_note:
        technique = graded["tags"][0] if graded["tags"] else problem_id
        journal = {"technique": technique, "note": method_note}
        note = "final answer matched"
    tick = None
    if graded["correct"]:
        node = _node_for_problem(problem_id, catalog, drills, session)
        if node is not None:
            preview = list(attempts) + [{"problem_id": problem_id, "correct": True}]
            if distinct_correct(node, drills, preview) >= 2 and not _solid(ticks, node["id"]):
                tick = {"node": node["id"], "status": "solid"}
    if open_match:
        new_session = _clear_to(session, updated)
    else:
        new_session = dict(session)
    retry = None
    if not graded["correct"]:
        node = _node_for_problem(problem_id, catalog, drills, session)
        if node is not None:
            alt = [row for row in candidates_for(node, drills) if row["id"] != problem_id]
            if alt:
                retry = drill_public(alt[0])
    say = "The final answer matches."
    if not graded["correct"]:
        unit = (graded["row"].get("unit") if graded["row"] else None) or "the matching unit"
        say = f"The final answer does not match. Teach one gap, then offer a drill from {unit}."
    if tick:
        say = f"{say} {tick['node']} is now solid."
    ledger, sticky = gap_rows(graded, problem_id, method_note)
    return {
        "exit": 0 if graded["correct"] else 1,
        "error": None,
        "session": new_session,
        "effects": {
            "attempt": {
                "problem_id": problem_id,
                "correct": graded["correct"],
                "note": note,
                "tags": graded["tags"],
                "submitted": submitted,
                "row": graded["row"] if graded["row"].get("answer_sympy") or graded["row"].get("unit") else {"id": problem_id},
            }
        },
        "drill": retry,
        "say": say,
        "mark": {
            "id": problem_id,
            "correct": graded["correct"],
            "idempotent": False,
            "expected_display": graded["display"],
            "source": source,
        },
        "tick": tick,
        "journal": journal,
        "ledger": ledger,
        "sticky": sticky,
    }


def _node_for_problem(problem_id: str, catalog: list[dict], drills: list[dict], session: dict) -> dict | None:
    if session.get("problem_id") == problem_id and session.get("node"):
        for node in catalog:
            if node["id"] == session["node"]:
                return node
    drill = find_drill(drills, problem_id)
    if drill is None:
        return None
    for node in teachable(catalog):
        if any(row["id"] == problem_id for row in candidates_for(node, drills)):
            return node
    return None


def _fail(session, code: int, error: str) -> dict:
    return {
        "exit": code,
        "error": error,
        "session": session,
        "effects": {},
        "drill": None,
        "say": error,
        "mark": None,
        "tick": None,
        "journal": None,
    }


def parse_mock01(text: str) -> list[dict]:
    doc = yaml.safe_load(text)
    return [{"id": row["id"], "source": row.get("source")} for row in doc["problems"]]


def parse_papers(text: str) -> list[dict]:
    doc = yaml.safe_load(text)
    papers = []
    for row in doc["papers"]:
        papers.append(
            {
                "year": int(row["year"]),
                "count": int(row["count"]),
                "duration_minutes": int(row.get("duration_minutes") or 120),
                "problems": row.get("problems"),
                "mark_scheme": row.get("mark_scheme"),
                "solutions": row.get("solutions"),
            }
        )
    return papers


def paper_on_disk(papers: list[dict], root_exists) -> list[dict]:
    out = []
    for paper in papers:
        view = {
            "year": paper.get("year"),
            "count": paper.get("count"),
            "duration_minutes": paper.get("duration_minutes") or 120,
            "problems": paper.get("problems"),
            "mark_scheme": paper.get("mark_scheme"),
            "solutions": paper.get("solutions"),
            "on_disk": bool(paper.get("problems") and root_exists(paper["problems"])),
        }
        out.append(view)
    return out
