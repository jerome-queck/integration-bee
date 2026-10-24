#!/usr/bin/env python3
"""Show the tracker races TLC reports, using the real CLI writer."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_control():
    path = ROOT / "scripts" / "control-integration-bee"
    loader = importlib.machinery.SourceFileLoader("control_integration_bee", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


MOD = load_control()
ROW = {"id": "U01-D01"}


def lost_attempt() -> None:
    directory = Path(tempfile.mkdtemp(prefix="ib-lost-"))
    barrier = threading.Barrier(2)
    real = MOD.write_json

    def wrapped(folder, name, doc):
        if name == "attempts" and Path(folder).resolve() == directory.resolve():
            barrier.wait(timeout=10)
        return real(folder, name, doc)

    MOD.write_json = wrapped
    errors: list[BaseException] = []

    def go(correct: bool) -> None:
        try:
            MOD.record_attempt(directory, ROW, correct, "race", ["u-sub"])
        except BaseException as exc:
            errors.append(exc)

    threads = [threading.Thread(target=go, args=(flag,)) for flag in (False, True)]
    try:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=15)
        other = [exc for exc in errors if not isinstance(exc, FileNotFoundError)]
        if other:
            raise SystemExit(f"lost-attempt repro failed: {other!r}")
        path = directory / "attempts.json"
        items = json.loads(path.read_text())["items"] if path.exists() else []
        # Two reads of an empty list each replace the file with one row.
        # The shared attempts.json.tmp name can also make one replace raise.
        if len(items) == 2 and not errors:
            raise SystemExit("overlapping checks kept both rows")
        if len(items) > 2:
            raise SystemExit(f"overlapping checks left {len(items)} rows")
    finally:
        MOD.write_json = real
    print(f"PASS overlapping checks left {len(items)} row(s)")


def sequential_attempts() -> None:
    directory = Path(tempfile.mkdtemp(prefix="ib-seq-"))
    MOD.record_attempt(directory, ROW, False, "first", ["u-sub"])
    MOD.record_attempt(directory, ROW, True, "second", ["u-sub"])
    items = MOD.read_json(directory, "attempts")["items"]
    if len(items) != 2:
        raise SystemExit(f"sequential checks kept {len(items)} rows")
    print("PASS sequential checks keep both rows")


def progress_clobber() -> None:
    directory = Path(tempfile.mkdtemp(prefix="ib-clobber-"))
    arrived = threading.Barrier(2)
    finished = threading.Barrier(2)
    real_project = MOD.project

    def project(folder, ticks, attempts, mocks):
        if threading.current_thread().name == "check":
            arrived.wait(timeout=10)
            finished.wait(timeout=10)
        return real_project(folder, ticks, attempts, mocks)

    MOD.project = project
    errors: list[BaseException] = []

    def tick() -> None:
        try:
            arrived.wait(timeout=10)
            ticks = MOD.read_json(directory, "skill-ticks")
            ids = {node["id"] for node in MOD.catalog()}
            ticks["ticks"]["basic-integration"] = {"status": "solid", "ts": MOD.now_iso()}
            err = MOD.model.tick_problem(ticks["ticks"], ids)
            if err:
                raise RuntimeError(err)
            MOD.write_json(directory, "skill-ticks", ticks)
            real_project(
                directory,
                ticks,
                MOD.read_json(directory, "attempts"),
                MOD.read_json(directory, "mocks"),
            )
            finished.wait(timeout=10)
        except BaseException as exc:
            errors.append(exc)

    def check() -> None:
        try:
            MOD.record_attempt(directory, ROW, False, "clobber", ["u-sub"])
        except BaseException as exc:
            errors.append(exc)

    ticker = threading.Thread(target=tick, name="tick")
    checker = threading.Thread(target=check, name="check")
    try:
        ticker.start()
        checker.start()
        ticker.join(timeout=15)
        checker.join(timeout=15)
        if errors:
            raise SystemExit(f"progress clobber repro failed: {errors!r}")
        stored = json.loads((directory / "skill-ticks.json").read_text())
        progress = json.loads((directory / "progress.local.json").read_text())
        file_status = stored["ticks"]["basic-integration"]["status"]
        projected = (progress.get("skill_ticks") or {}).get("basic-integration") or {}
        if file_status != "solid" or projected.get("status") == "solid":
            raise SystemExit(
                f"progress clobber: skill-ticks={file_status} progress={projected}"
            )
    finally:
        MOD.project = real_project
    print("PASS progress dropped the solid tick")


def crash_after_attempt() -> None:
    directory = Path(tempfile.mkdtemp(prefix="ib-crash-"))
    attempts = MOD.read_json(directory, "attempts")
    item = {
        "ts": MOD.now_iso(),
        "problem_id": ROW["id"],
        "correct": False,
        "tags": ["u-sub"],
        "note": "stopped after the attempts write",
        **MOD.model.next_srs(None, False, MOD.today()),
    }
    err = MOD.model.attempt_problem(item)
    if err:
        raise SystemExit(err)
    attempts["items"].append(item)
    MOD.write_json(directory, "attempts", attempts)
    heat = MOD.read_json(directory, "heatmap")
    if heat.get("topics"):
        raise SystemExit(f"heatmap changed after a stop at the attempts write: {heat}")
    if (directory / "progress.local.json").exists():
        raise SystemExit("progress.local.json exists after a stop at the attempts write")
    if len(MOD.read_json(directory, "attempts")["items"]) != 1:
        raise SystemExit("the attempts write did not stick")
    print("PASS stop after the attempts write leaves heatmap and progress behind")


def main() -> None:
    sequential_attempts()
    lost_attempt()
    progress_clobber()
    crash_after_attempt()


if __name__ == "__main__":
    main()
