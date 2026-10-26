from __future__ import annotations

import check_math
import gap_index
import model
import problem_catalog
import sympy as sp
import yaml

PHASE_IDLE = "idle"
PHASE_AWAITING = "awaiting_answer"
PHASE_MOCK = "mock_open"
PHASE_MOCK_Q = "mock_awaiting"
PHASE_APTITUDE = "aptitude"
PHASE_PROPOSING = "proposing"
DETAIL = ("worked", "faded", "bare")
LOST_PROBES = frozenset({"YANG-1.3-Ex01", "YANG-1.3-Ex03"})


def empty_session() -> dict:
    return {
        "schema": "integration-bee-session/v1",
        "phase": PHASE_IDLE,
        "node": None,
        "problem_id": None,
        "mock_id": None,
        "updated": None,
        "aptitude": {"full_coverage": False, "offer": [], "declined": []},
        "policy": {},
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


def recommend_node(
    catalog: list[dict],
    ticks: dict,
    heat: dict,
    drills: list[dict],
    full_coverage: bool = False,
) -> dict | None:
    nodes = teachable(catalog)
    tagged = [(node, node_tags(node, drills)) for node in nodes]
    for topic in weak_topics(heat):
        for node, tags in tagged:
            if topic["tag"] in tags and not model.coach_queue_done(_status(ticks, node["id"]), full_coverage):
                return node
    for node, _tags in tagged:
        if not model.coach_queue_done(_status(ticks, node["id"]), full_coverage):
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


def _choose_drill(rows: list[dict], attempts: list[dict]) -> dict | None:
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


def pick_drill(node: dict, drills: list[dict], attempts: list[dict]) -> dict | None:
    return _choose_drill(candidates_for(node, drills), attempts)


def _coverage(session: dict) -> bool:
    aptitude = session.get("aptitude")
    if not isinstance(aptitude, dict):
        return False
    return aptitude.get("full_coverage") is True


def _id_copy(value) -> list:
    if not isinstance(value, list):
        return []
    return list(value)


def _stored_aptitude(session: dict) -> dict:
    current = session.get("aptitude")
    if not isinstance(current, dict):
        return {"full_coverage": False, "offer": [], "declined": []}
    full = current.get("full_coverage", False)
    return {
        "full_coverage": full,
        "offer": _id_copy(current.get("offer", [])),
        "declined": _id_copy(current.get("declined", [])),
    }


def _stored_policy(session: dict) -> dict:
    current = session.get("policy")
    if not isinstance(current, dict):
        return {}
    out = {}
    for key, row in current.items():
        out[key] = dict(row) if isinstance(row, dict) else row
    return out


def _drill_kind(row: dict) -> str:
    kind = row.get("kind")
    if kind in {"definite", "indefinite"}:
        return kind
    limits = row.get("limits")
    if limits in (None, []):
        return "indefinite"
    return "definite"


def _techniques(rows: list[dict]) -> list[str]:
    found = []
    for row in rows:
        tech = row.get("technique") or "any"
        if tech not in found:
            found.append(tech)
    return found or ["any"]


def contest_probe_id(records: list[dict]) -> str | None:
    for row in records:
        if row.get("round") != "r1" or row.get("verify") != "manual":
            continue
        if not row.get("answer_plain"):
            continue
        if row.get("answer_sympy") or row.get("integrand_latex"):
            continue
        if row.get("id") in LOST_PROBES:
            continue
        return row.get("id")
    return None


def _has_attempt(attempts: list[dict], ids: set[str]) -> bool:
    return any(item.get("problem_id") in ids for item in attempts)


def _pending_drills(attempts, ticks, catalog, drills, full_coverage: bool) -> list[dict]:
    pending = []
    for node in teachable(catalog):
        if node.get("gate") != "round1":
            continue
        if model.coach_queue_done(_status(ticks, node["id"]), full_coverage):
            continue
        rows = candidates_for(node, drills)
        if not rows:
            continue
        if _has_attempt(attempts, {row["id"] for row in rows}):
            continue
        pending.append({"source": "drill", "problem_id": rows[0]["id"], "node": node["id"]})
    return pending


def _any_round1_drill_attempt(attempts, catalog, drills) -> bool:
    for node in teachable(catalog):
        if node.get("gate") != "round1":
            continue
        ids = {row["id"] for row in candidates_for(node, drills)}
        if ids and _has_attempt(attempts, ids):
            return True
    return False


def next_probe(attempts, ticks, catalog, drills, records, full_coverage: bool) -> dict | None:
    pending = _pending_drills(attempts, ticks, catalog, drills, full_coverage)
    contest = contest_probe_id(records)
    contest_open = bool(contest) and not _has_attempt(attempts, {contest})
    if pending and not _any_round1_drill_attempt(attempts, catalog, drills):
        return pending[0]
    if contest_open:
        return {"source": "catalog", "problem_id": contest, "node": None}
    if pending:
        return pending[0]
    return None


def skip_offer(attempts, ticks, catalog, drills, declined: set[str] | None = None) -> list[str]:
    correct = {item.get("problem_id") for item in attempts if item.get("correct") is True}
    blocked = declined or set()
    offer = []
    for node in teachable(catalog):
        if node["id"] in blocked:
            continue
        status = _status(ticks, node["id"])
        if status in {"solid", "skipped"}:
            continue
        ids = {row["id"] for row in candidates_for(node, drills)}
        if correct & ids:
            offer.append(node["id"])
    return offer


def default_policy(node: dict, drills: list[dict], full_coverage: bool) -> dict:
    rows = candidates_for(node, drills)
    kinds = {_drill_kind(row) for row in rows}
    if "definite" in kinds:
        kind = "definite"
    elif len(kinds) == 1:
        kind = next(iter(kinds))
    else:
        kind = "any"
    approach = rows[0].get("technique") if rows and rows[0].get("technique") else "any"
    volume = len(rows) if full_coverage else min(2, len(rows))
    return {"approach": approach, "detail": "worked", "kind": kind, "volume": volume}


def step_policy(row: dict, correct: bool, drill: dict, rows: list[dict], solid_now: bool) -> dict:
    try:
        index = DETAIL.index(row["detail"])
    except ValueError:
        index = 0
    if correct:
        index = min(index + 1, len(DETAIL) - 1)
    else:
        index = max(index - 1, 0)
    volume = row.get("volume", 0)
    if isinstance(volume, bool) or not isinstance(volume, int):
        volume = 0
    if correct:
        volume = 0 if solid_now else max(1, volume - 1)
    else:
        volume = min(len(rows), volume + 1)
    approach = row["approach"]
    kind = row["kind"]
    if not correct:
        techs = _techniques(rows)
        if approach in techs:
            approach = techs[(techs.index(approach) + 1) % len(techs)]
        else:
            approach = techs[0]
        kinds = {_drill_kind(item) for item in rows}
        if "definite" in kinds and "indefinite" in kinds:
            if kind == "indefinite":
                kind = "definite"
            else:
                kind = "indefinite"
    return {"approach": approach, "detail": DETAIL[index], "kind": kind, "volume": volume}


def policy_for(session: dict, node: dict, drills: list[dict]) -> dict | None:
    row = (session.get("policy") or {}).get(node["id"])
    if not isinstance(row, dict):
        return None
    return dict(row)


def pick_coached(node, row, drills, attempts) -> dict | None:
    rows = candidates_for(node, drills)
    correct = {item.get("problem_id") for item in attempts if item.get("correct") is True}

    def matching(use_kind: bool) -> list[dict]:
        pool = []
        for drill in rows:
            tech = drill.get("technique") or "any"
            if row.get("approach") not in {None, "any"} and tech != row.get("approach"):
                continue
            if use_kind and row.get("kind") not in {None, "any"} and _drill_kind(drill) != row.get("kind"):
                continue
            pool.append(drill)
        return pool

    pool = matching(True)
    if not any(drill["id"] not in correct for drill in pool):
        pool = matching(False)
    if not any(drill["id"] not in correct for drill in pool):
        pool = rows
    return _choose_drill(pool, attempts)


def _catalog_rows(records: list[dict] | None) -> list[dict]:
    if records is not None:
        return records
    return problem_catalog.load_records()


def _probe_payload(probe: dict, drills: list[dict], records: list[dict]) -> tuple[dict | None, list | None, str]:
    if probe.get("source") == "catalog" or not probe.get("node"):
        row = next((item for item in records if item.get("id") == probe.get("problem_id")), None)
        problems = [problem_catalog.prompt_view(row)] if row else None
        say = "A contest integral is open. Ask for written working. Do not invent an answer."
        return None, problems, say
    drill = find_drill(drills, probe["problem_id"])
    view = drill_public(drill) if drill else {"id": probe["problem_id"]}
    say = "An aptitude integral is open. Ask for written working. Do not show an answer."
    return view, None, say


def describe_open_probe(session: dict, drills: list[dict], records: list[dict]) -> tuple[dict | None, list | None, str]:
    probe = {
        "source": "drill" if session.get("node") else "catalog",
        "problem_id": session.get("problem_id"),
        "node": session.get("node"),
    }
    return _probe_payload(probe, drills, records)


def _requested_gap(extract: dict):
    if "gap" not in extract:
        return None, None
    index, err = gap_index.load_index()
    if err or index is None:
        return None, err or "gap index is unreadable"
    return gap_index.parse_gap(extract.get("gap"), index)


def _stored_gap(gap_id: str):
    index, err = gap_index.load_index()
    if err or index is None:
        return None, err or "gap index is unreadable"
    return gap_index.parse_gap(gap_id, index)


def find_drill(drills: list[dict], drill_id: str) -> dict | None:
    for row in drills:
        if row["id"] == drill_id:
            return row
    return None


def coach_view(catalog: list[dict], ticks: dict, heat: dict, drills: list[dict], session: dict | None = None) -> dict:
    session = session or {}
    aptitude = session.get("aptitude") if isinstance(session.get("aptitude"), dict) else {}
    full = aptitude.get("full_coverage") is True
    node = recommend_node(catalog, ticks, heat, drills, full_coverage=full)
    gate = readiness(catalog, ticks)
    offer = list(aptitude.get("offer") or []) if session.get("phase") == PHASE_PROPOSING else []
    row = None
    if node is not None:
        stored = (session.get("policy") or {}).get(node["id"]) if isinstance(session.get("policy"), dict) else None
        if isinstance(stored, dict):
            row = stored
    return {
        "next_node": node["id"] if node else None,
        "unit": node.get("unit") if node else None,
        "teaching": f"units/{node['unit']}/teaching.tex" if node else None,
        "ready": gate["ready"],
        "missing_round1": gate["missing_round1"],
        "weak": weak_topics(heat),
        "offer": offer,
        "full_coverage": full,
        "approach": row.get("approach") if row else None,
        "detail": row.get("detail") if row else None,
        "kind": row.get("kind") if row else None,
        "volume": row.get("volume") if row else None,
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


def expressions_match(answer: str, submitted: str, indefinite: bool, variable: str = "x") -> bool:
    ns = _mark_namespace()
    ns[variable] = sp.Symbol(variable, real=True)
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
    return sp.simplify(sp.diff(got - ans, ns[variable])) == 0


def _indefinite(row: dict) -> bool:
    if row.get("kind") == "indefinite":
        return True
    limits = row.get("limits")
    return limits in (None, [])


def answer_matches(row: dict, submitted: str) -> bool:
    return expressions_match(row["answer_sympy"], submitted, _indefinite(row), row.get("variable", "x"))


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
    catalog_row = next((row for row in (catalog_rows or []) if row.get("id") == problem_id), None)
    feed_row = next((row for row in feed if row.get("id") == problem_id), None)
    if catalog_row is not None:
        if catalog_row.get("verify") == "sympy":
            answer = catalog_row.get("answer_sympy")
            variable = catalog_row.get("variable")
            if not isinstance(answer, str) or not answer or variable not in problem_catalog.SYMPY_VARIABLES:
                return None, "catalog problem is not sympy-checked"
            try:
                correct = expressions_match(answer, submitted, _indefinite(catalog_row), variable)
            except Exception as exc:
                return None, f"answer did not parse: {exc}"
            tags = list(catalog_row.get("technique_tags") or [])
            tags.extend(catalog_row.get("yang") or [])
            return {
                "correct": correct,
                "tags": tags,
                "display": catalog_row.get("answer_latex") or answer,
                "row": {
                    "id": problem_id,
                    "answer_sympy": answer,
                    "kind": catalog_row.get("kind"),
                    "limits": catalog_row.get("limits"),
                    "variable": variable,
                },
                "manual": False,
            }, None
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
    if feed_row is None:
        return None, f"unknown problem {problem_id}"
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


def _set_phase(session, phase, node, problem_id, mock_id, updated, aptitude=None, policy=None) -> dict:
    doc = {
        "schema": "integration-bee-session/v1",
        "phase": phase,
        "node": node,
        "problem_id": problem_id,
        "mock_id": mock_id,
        "updated": updated,
        "aptitude": _stored_aptitude({"aptitude": aptitude}) if aptitude is not None else _stored_aptitude(session),
        "policy": _stored_policy({"policy": policy}) if policy is not None else _stored_policy(session),
    }
    err = model.session_problem(doc)
    if err:
        raise ValueError(err)
    return doc


def _clear_to(session: dict, updated: str, policy=None) -> dict:
    if session.get("mock_id") and session.get("phase") in {PHASE_MOCK, PHASE_MOCK_Q}:
        return _set_phase(session, PHASE_MOCK, None, None, session["mock_id"], updated, policy=policy)
    if session.get("phase") == PHASE_PROPOSING:
        return _set_phase(session, PHASE_PROPOSING, None, None, None, updated, policy=policy)
    return _set_phase(session, PHASE_IDLE, None, None, None, updated, policy=policy)


def _hold(session: dict, updated: str, policy=None) -> dict:
    return _set_phase(
        session,
        session.get("phase") or PHASE_IDLE,
        session.get("node"),
        session.get("problem_id"),
        session.get("mock_id"),
        updated,
        policy=policy,
    )


def distinct_correct(node: dict, drills: list[dict], attempts: list[dict]) -> int:
    ids = {row["id"] for row in candidates_for(node, drills)}
    got = set()
    for item in attempts:
        if item.get("correct") is True and item.get("problem_id") in ids:
            got.add(item["problem_id"])
    return len(got)


def _teach_say(node: dict, row: dict | None) -> str:
    if row is None:
        return f"Teach {node['id']} from units/{node['unit']}/teaching.tex. Then set this integral."
    if row.get("detail") == "faded":
        return "Give one faded step, then this integral."
    if row.get("detail") == "bare":
        return "Set this integral. Do not show a worked example."
    return "Give the worked example, then a faded step, then this integral."


def _queue_say(catalog: list[dict], ticks: dict) -> str:
    if readiness(catalog, ticks)["ready"]:
        return "Every teachable node is solid. Offer a mock or a due review."
    return (
        "The default queue is clear. Skipped Round 1 nodes still block the mock. "
        "Ask for full coverage or teach a skipped node until it is solid."
    )


def plan_teach(session, attempts, ticks, catalog, drills, heat, updated: str, records=None) -> dict:
    phase = session.get("phase") or PHASE_IDLE
    if phase == PHASE_PROPOSING:
        return _fail(session, 2, "confirm the skip offer first")
    if phase == PHASE_APTITUDE:
        if not session.get("problem_id"):
            return _fail(session, 2, "aptitude session needs a problem")
        drill, problems, _ = describe_open_probe(session, drills, _catalog_rows(records))
        return {
            "exit": 0,
            "error": None,
            "session": session,
            "effects": {},
            "drill": drill,
            "problems": problems,
            "say": "The same integral is still open. Show it again. Do not show an answer.",
            "mark": None,
            "tick": None,
            "ticks": [],
        }
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
        return _fail(session, 2, "a mock is open")
    node = recommend_node(catalog, ticks, heat, drills, full_coverage=_coverage(session))
    if node is None:
        return {
            "exit": 0,
            "error": None,
            "session": session,
            "effects": {},
            "drill": None,
            "say": _queue_say(catalog, ticks),
            "mark": None,
            "tick": None,
        }
    row = policy_for(session, node, drills)
    drill = pick_drill(node, drills, attempts) if row is None else pick_coached(node, row, drills, attempts)
    if drill is None:
        return _fail(session, 2, f"no drill for {node['id']}")
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
        "say": _teach_say(node, row),
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


def _ok(
    session,
    say,
    drill=None,
    problems=None,
    mark=None,
    tick=None,
    ticks=None,
    effects=None,
    journal=None,
    ledger=None,
    sticky=None,
    exit_code=0,
) -> dict:
    if ticks is None:
        ticks = [tick] if tick else []
    return {
        "exit": exit_code,
        "error": None,
        "session": session,
        "effects": effects or {},
        "drill": drill,
        "problems": problems,
        "say": say,
        "mark": mark,
        "tick": tick,
        "ticks": ticks,
        "journal": journal,
        "ledger": ledger,
        "sticky": sticky,
    }


def _offer_say(offer: list[str]) -> str:
    ids = ", ".join(offer)
    return (
        f"These nodes can be skipped: {ids}. "
        "Nothing is skipped until a confirm turn repeats the ids."
    )


def _open_probe(session, probe, drills, records, updated, policy):
    new_session = _set_phase(
        session,
        PHASE_APTITUDE,
        probe["node"],
        probe["problem_id"],
        None,
        updated,
        policy=policy,
    )
    drill, problems, say = _probe_payload(probe, drills, records)
    return new_session, drill, problems, say


def _finish_placement(session, attempts, ticks, catalog, drills, records, updated, policy, correct: bool):
    if not correct:
        new_session = _set_phase(session, PHASE_IDLE, None, None, None, updated, policy=policy)
        return new_session, None, None, None
    declined = set(_stored_aptitude(session)["declined"])
    probe = next_probe(attempts, ticks, catalog, drills, records, _coverage(session))
    if probe and probe.get("source") == "catalog":
        return _open_probe(session, probe, drills, records, updated, policy)
    offer = skip_offer(attempts, ticks, catalog, drills, declined)
    if offer:
        aptitude = _stored_aptitude(session)
        aptitude["offer"] = offer
        new_session = _set_phase(
            session, PHASE_PROPOSING, None, None, None, updated, aptitude=aptitude, policy=policy
        )
        return new_session, None, None, _offer_say(offer)
    if probe:
        return _open_probe(session, probe, drills, records, updated, policy)
    new_session = _set_phase(session, PHASE_IDLE, None, None, None, updated, policy=policy)
    return new_session, None, None, None


def _mark_decision(problem_id, graded, attempts, ticks, catalog, drills, session, include_new: bool):
    seen = list(attempts)
    if include_new:
        seen.append({"problem_id": problem_id, "correct": graded["correct"]})
    drill_row = find_drill(drills, problem_id)
    node = _node_for_problem(problem_id, catalog, drills, session) if drill_row is not None and not graded["manual"] else None
    tick = None
    if node is not None and graded["correct"]:
        if distinct_correct(node, drills, seen) >= 2 and not _solid(ticks, node["id"]):
            tick = {"node": node["id"], "status": "solid"}
    elif node is not None and _status(ticks, node["id"]) == "skipped":
        tick = {"node": node["id"], "status": "learning"}
    policy = None
    if node is not None and drill_row is not None:
        policy = _stored_policy(session)
        current = policy.get(node["id"])
        rows = candidates_for(node, drills)
        base = current if isinstance(current, dict) else default_policy(node, drills, _coverage(session))
        solid_now = bool(graded["correct"]) and (
            _solid(ticks, node["id"]) or (tick is not None and tick.get("status") == "solid")
        )
        policy[node["id"]] = step_policy(base, bool(graded["correct"]), drill_row, rows, solid_now)
    return seen, tick, node, policy


def plan_aptitude(session, attempts, ticks, catalog, drills, records, updated: str) -> dict:
    phase = session.get("phase") or PHASE_IDLE
    rows = _catalog_rows(records)
    if phase == PHASE_APTITUDE:
        if not session.get("problem_id"):
            return _fail(session, 2, "aptitude session needs a problem")
        drill, problems, say = describe_open_probe(session, drills, rows)
        return _ok(session, say, drill=drill, problems=problems)
    if phase == PHASE_PROPOSING:
        return _fail(session, 2, "confirm the skip offer first")
    if phase == PHASE_AWAITING:
        return _fail(session, 2, "an integral is still open")
    if phase in {PHASE_MOCK, PHASE_MOCK_Q}:
        return _fail(session, 2, "a mock is open")
    if phase != PHASE_IDLE:
        return _fail(session, 2, "aptitude is not open")
    probe = next_probe(attempts, ticks, catalog, drills, rows, _coverage(session))
    if probe is None:
        declined = set(_stored_aptitude(session)["declined"])
        offer = skip_offer(attempts, ticks, catalog, drills, declined)
        if offer:
            aptitude = _stored_aptitude(session)
            aptitude["offer"] = offer
            new_session = _set_phase(session, PHASE_PROPOSING, None, None, None, updated, aptitude=aptitude)
            return _ok(new_session, _offer_say(offer))
        return _ok(session, "No placement probe is open.")
    new_session = _set_phase(session, PHASE_APTITUDE, probe["node"], probe["problem_id"], None, updated)
    drill, problems, say = _probe_payload(probe, drills, rows)
    return _ok(new_session, say, drill=drill, problems=problems)


def _merge_ids(current: list[str], extra: list[str]) -> list[str]:
    merged = list(current)
    seen = set(merged)
    for node_id in extra:
        if node_id not in seen:
            merged.append(node_id)
            seen.add(node_id)
    return merged


def _confirm_nodes(body: dict) -> list[str] | None:
    nodes = body.get("nodes")
    if not isinstance(nodes, list):
        return None
    named = []
    seen = set()
    for item in nodes:
        if not isinstance(item, str) or item == "":
            return None
        if item in seen:
            continue
        seen.add(item)
        named.append(item)
    return named


def _confirm_say(ids: list[str], full: bool) -> str:
    if not ids:
        return "No nodes were skipped. Teach the next node."
    joined = ", ".join(ids)
    if full:
        return (
            f"Skipped {joined}. Full coverage is on, so the coach still teaches them. "
            "The mock still needs them solid."
        )
    return f"Skipped {joined}. The coach will leave them until a miss on that node or full coverage."


def plan_confirm(session, ticks, catalog, body: dict, updated: str) -> dict:
    named = _confirm_nodes(body)
    if named is None:
        return _fail(session, 2, "confirm needs a list of node ids")
    offer = _stored_aptitude(session)["offer"]
    if any(node_id not in offer for node_id in named):
        return _fail(session, 2, "confirm names a node the offer left out")
    phase = session.get("phase")
    if phase == PHASE_PROPOSING:
        aptitude = _stored_aptitude(session)
        if not named:
            aptitude["declined"] = _merge_ids(aptitude["declined"], offer)
            aptitude["offer"] = []
            new_session = _set_phase(session, PHASE_IDLE, None, None, None, updated, aptitude=aptitude)
            return _ok(new_session, "No nodes were skipped. Teach the next node.")
        chosen = set(named)
        aptitude["declined"] = _merge_ids(
            aptitude["declined"],
            [node_id for node_id in offer if node_id not in chosen],
        )
        kept = [node_id for node_id in offer if node_id in chosen]
        tick_list = []
        for node_id in kept:
            if _status(ticks, node_id) in {None, "learning"}:
                tick_list.append({"node": node_id, "status": "skipped"})
        aptitude["offer"] = kept
        new_session = _set_phase(session, PHASE_IDLE, None, None, None, updated, aptitude=aptitude)
        skipped_ids = [node_id for node_id in kept if _status(ticks, node_id) != "solid"]
        return _ok(new_session, _confirm_say(skipped_ids, _coverage(session)), ticks=tick_list)
    if phase == PHASE_IDLE and all(_status(ticks, node_id) in {"solid", "skipped"} for node_id in named):
        return _ok(session, "No nodes were skipped. Teach the next node.")
    return _fail(session, 2, "confirm is not open")


def plan_cover(session, catalog, drills, body: dict, updated: str) -> dict:
    if "full" in body and not isinstance(body.get("full"), bool):
        return _fail(session, 2, "cover needs a bool")
    full = True if "full" not in body else body["full"]
    aptitude = _stored_aptitude(session)
    policy = _stored_policy(session)
    if full and aptitude["full_coverage"] is not True:
        by_id = {node["id"]: node for node in catalog}
        for node_id, row in list(policy.items()):
            node = by_id.get(node_id)
            if node is None or not isinstance(row, dict):
                continue
            revised = dict(row)
            revised["volume"] = max(int(row["volume"]), len(candidates_for(node, drills)))
            policy[node_id] = revised
    aptitude["full_coverage"] = full
    new_session = _set_phase(
        session,
        session.get("phase") or PHASE_IDLE,
        session.get("node"),
        session.get("problem_id"),
        session.get("mock_id"),
        updated,
        aptitude=aptitude,
        policy=policy,
    )
    if full:
        say = "Full coverage is on. The coach teaches skipped nodes again. The mock still needs every Round 1 node solid."
    else:
        say = "Full coverage is off. Confirmed skips leave the coach queue."
    return _ok(new_session, say)


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
    gap, gap_err = _requested_gap(extract)
    if gap_err:
        return _fail(session, 2, gap_err)
    graded, err = grade_problem(problem_id, submitted, verdict, drills, feed, catalog_rows)
    if err:
        return _fail(session, 2, err)
    if session.get("phase") == PHASE_APTITUDE and session.get("problem_id") != problem_id:
        return _fail(session, 2, f"the open integral is {session.get('problem_id')}")
    latest = _latest(attempts, problem_id)
    same_answer = bool(
        latest
        and latest.get("submitted") == submitted
        and latest.get("correct") is graded["correct"]
    )
    open_match = session.get("problem_id") == problem_id and session.get("phase") in {PHASE_AWAITING, PHASE_MOCK_Q}
    if open_match and same_answer:
        incoming = gap.id if gap is not None else None
        repeat = gap_index.classify_repeat(latest.get("gap"), incoming)
        if repeat is gap_index.Repeat.REJECT:
            return _fail(session, 2, "gap does not match the recorded gap")
        if repeat is gap_index.Repeat.FILL and graded["correct"] and not method_note:
            return _fail(session, 2, "correct mark needs method_note when gap is set")
        new_session = _clear_to(session, updated)
        tick = None
        node = _node_for_problem(problem_id, catalog, drills, session)
        if node is not None and graded["correct"]:
            if distinct_correct(node, drills, attempts) >= 2 and not _solid(ticks, node["id"]):
                tick = {"node": node["id"], "status": "solid"}
        elif node is not None and _status(ticks, node["id"]) == "skipped":
            tick = {"node": node["id"], "status": "learning"}
        ledger, sticky = gap_rows(graded, problem_id, method_note) if method_note else (None, None)
        effects = {}
        if repeat is gap_index.Repeat.FILL:
            effects = {"gap_fill": {"problem_id": problem_id, "gap": gap.id}}
        say = "That mark was already recorded."
        resolved = gap
        if resolved is None and latest.get("gap"):
            resolved, stored_err = _stored_gap(latest["gap"])
            if stored_err:
                return _fail(session, 2, stored_err)
        if resolved is not None:
            unit = (graded.get("row") or {}).get("unit")
            say = f"{say} {gap_index.note_say(unit, resolved, graded['correct'])}"
        return {
            "exit": 0 if graded["correct"] else 1,
            "error": None,
            "session": new_session,
            "effects": effects,
            "drill": None,
            "say": say,
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
    if gap is not None and graded["correct"] and not method_note:
        return _fail(session, 2, "correct mark needs method_note when gap is set")
    aptitude_same = session.get("phase") == PHASE_APTITUDE and same_answer
    seen, tick, node, policy = _mark_decision(
        problem_id,
        graded,
        attempts,
        ticks,
        catalog,
        drills,
        session,
        include_new=not aptitude_same,
    )
    note = "final answer matched" if graded["correct"] else "final answer differed"
    if graded["manual"]:
        note = "manual mark"
    journal = None
    if not aptitude_same and graded["correct"] and method_note:
        technique = graded["tags"][0] if graded["tags"] else problem_id
        journal = {"technique": technique, "note": method_note}
        note = "final answer matched"
    if aptitude_same:
        ledger, sticky = gap_rows(graded, problem_id, method_note) if method_note else (None, None)
        effects = {}
    else:
        ledger, sticky = gap_rows(graded, problem_id, method_note)
        stored_row = graded["row"] if graded["row"].get("answer_sympy") or graded["row"].get("unit") else {"id": problem_id}
        effects = {
            "attempt": {
                "problem_id": problem_id,
                "correct": graded["correct"],
                "note": note,
                "tags": graded["tags"],
                "submitted": submitted,
                "row": stored_row,
            }
        }
        if gap is not None:
            effects["attempt"]["gap"] = gap.id
    phase = session.get("phase")
    problems = None
    extra = None
    drill_view = None
    if phase == PHASE_APTITUDE:
        records = _catalog_rows(catalog_rows)
        new_session, drill_view, problems, extra = _finish_placement(
            session, seen, ticks, catalog, drills, records, updated, policy, graded["correct"]
        )
    elif open_match or phase == PHASE_PROPOSING:
        new_session = _clear_to(session, updated, policy=policy)
    else:
        new_session = _hold(session, updated, policy=policy)
    if phase != PHASE_APTITUDE and not graded["correct"] and node is not None:
        alt = [row for row in candidates_for(node, drills) if row["id"] != problem_id]
        if alt:
            drill_view = drill_public(alt[0])
    say = "That mark was already recorded." if aptitude_same else None
    if say is None:
        unit = (graded.get("row") or {}).get("unit")
        say = gap_index.note_say(unit, gap, graded["correct"])
    if tick and tick.get("status") == "solid":
        say = f"{say} {tick['node']} is now solid."
    if extra:
        say = f"{say} {extra}"
    return {
        "exit": 0 if graded["correct"] else 1,
        "error": None,
        "session": new_session,
        "effects": effects,
        "drill": drill_view,
        "problems": problems,
        "say": say,
        "mark": {
            "id": problem_id,
            "correct": graded["correct"],
            "idempotent": aptitude_same,
            "expected_display": graded["display"],
            "source": source,
        },
        "tick": tick,
        "ticks": [tick] if tick else [],
        "journal": journal,
        "ledger": ledger,
        "sticky": sticky,
    }


def _node_for_problem(problem_id: str, catalog: list[dict], drills: list[dict], session: dict) -> dict | None:
    if find_drill(drills, problem_id) is None:
        return None
    if session.get("problem_id") == problem_id and session.get("node"):
        for node in catalog:
            if node["id"] == session["node"]:
                return node
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
        "problems": None,
        "say": error,
        "mark": None,
        "tick": None,
        "ticks": [],
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
