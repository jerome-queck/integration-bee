#!/usr/bin/env python3
"""Build Yang Ch.3–6.9 concept units (19–37). SymPy-verify with per-drill timeout."""
from __future__ import annotations

import json
import multiprocessing as mp
import re
import sys
import traceback
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "units"
VERIFY = ROOT / "verify"
AUDIT = ROOT / ".audit"


def _retired() -> None:
    print(
        "build_yang_ch3_to_ch6 is retired and does not rewrite units, drills, or indexes. "
        "The old generator called unrestricted sympify and accepted a numeric shortcut.",
        file=sys.stderr,
    )
    raise SystemExit(2)

NS = {
    "x": sp.symbols("x", real=True),
    "pi": sp.pi, "exp": sp.exp, "log": sp.log,
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "sec": sp.sec, "csc": sp.csc, "cot": sp.cot,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sqrt": sp.sqrt, "Abs": sp.Abs, "E": sp.E, "oo": sp.oo,
    "Rational": sp.Rational, "asinh": sp.asinh,
    "sinh": sp.sinh, "cosh": sp.cosh,
    "Catalan": sp.Catalan,
}
x = NS["x"]


def _worker(payload, q):
    try:
        d = payload
        expr = sp.sympify(d["sympy_expr"], locals=NS)
        ans = sp.sympify(d["answer_sympy"], locals=NS)
        if d["kind"] == "definite":
            lo = sp.sympify(d["limits"][0], locals=NS)
            hi = sp.sympify(d["limits"][1], locals=NS)
            val = sp.integrate(expr, (x, lo, hi)).simplify()
            if sp.simplify(val - ans) != 0:
                try:
                    if abs(complex(sp.N(val - ans))) < 1e-8:
                        q.put(("ok", None)); return
                except Exception:
                    pass
                q.put(("fail", f"got {val}, expected {ans}")); return
        else:
            if sp.simplify(sp.diff(ans, x) - expr) != 0:
                q.put(("fail", "d/dx mismatch")); return
        q.put(("ok", None))
    except Exception as e:
        q.put(("fail", f"{type(e).__name__}: {e}"))


def verify_timeout(d: dict, timeout: float = 12.0) -> None:
    _retired()
    if d.get("verify_mode") == "numeric":
        expr = sp.sympify(d["sympy_expr"], locals=NS)
        ans = sp.sympify(d["answer_sympy"], locals=NS)
        lo = sp.sympify(d["limits"][0], locals=NS)
        hi = sp.sympify(d["limits"][1], locals=NS)
        nval = sp.N(sp.Integral(expr, (x, lo, hi)))
        if abs(complex(nval - sp.N(ans))) > 1e-6:
            raise AssertionError(f"{d['id']}: numeric {nval} != {ans}")
        return
    q: mp.Queue = mp.Queue()
    p = mp.Process(target=_worker, args=(d, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate(); p.join(1)
        raise TimeoutError(f"{d['id']}: SymPy hung >{timeout}s")
    if q.empty():
        raise RuntimeError(f"{d['id']}: no result")
    status, msg = q.get()
    if status != "ok":
        raise AssertionError(f"{d['id']}: {msg}")


def mk(id_, tech, yang, kind, latex, se, hint, limits=None, ans=None, disp=None, verify_mode=None):
    assert ans is not None
    d = {
        "id": id_, "technique": tech, "kind": kind, "latex": latex,
        "sympy_expr": se, "answer_sympy": ans,
        "answer_display": disp if disp is not None else ans,
        "hint": hint, "technique_tags": [tech, yang], "yang": [yang],
    }
    if limits is not None:
        d["limits"] = limits
    if verify_mode is not None:
        d["verify_mode"] = verify_mode
    # pretty display via latex if still raw
    if disp is None:
        try:
            a = sp.sympify(ans, locals=NS)
            d["answer_display"] = sp.latex(a) + ("+C" if kind == "indefinite" else "")
        except Exception:
            pass
    verify_timeout(d)
    return d


def write_unit(meta, drills):
    _retired()
    uid, order = meta["uid"], meta["order"]
    udir = UNITS / uid
    udir.mkdir(parents=True, exist_ok=True)
    for d in drills:
        d["unit"] = uid
        d.setdefault("solution_note", d.get("hint", ""))

    yang, tech = meta["yang"], meta["tech"]
    lines = [
        f'unit_id: "{uid}"', f'title: "{meta["title"]}"', f"order: {order}",
        "kind: concept", "status: ready", "past_paper: false",
        f'problem_id_prefix: "U{order:02d}-D"', "technique_tags:",
    ]
    lines += [f"  - {t}" for t in tech]
    lines += ["yang_tags:"] + [f'  - "{y}"' for y in yang]
    lines += [
        "syllabus_refs:",
        "  - source: user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf",
        f'    section: "{meta["section"]}"',
        "  - source: UK_University_Integration_Bee_Syllabus.pdf",
        '    section: "§1 Integration Techniques (supporting)"',
        "prerequisites:",
    ]
    lines += [f'  - "{p}"' for p in meta.get("prereq", [])]
    lines += [
        "files:",
        "  teaching_tex: teaching.tex",
        "  drills_tex: drills.tex",
        "  solutions_tex: solutions.tex",
        "  drills_feed: drills.md",
        f"  machine_drills: ../../verify/drills_unit{order}.json",
        'latex_note: "Self-contained article-class until templates/ lands; then switch."',
        "",
    ]
    (udir / "meta.yaml").write_text("\n".join(lines))

    ytex = ", ".join(rf"\texttt{{{y}}}" for y in yang)
    ttex = ", ".join(rf"\texttt{{{t}}}" for t in tech)
    sec = meta["section"].replace("_", r"\_")
    (udir / "teaching.tex").write_text(
        f"""% Unit {order:02d} — {meta['title']}
\\documentclass[11pt]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{hyperref}}
\\title{{Integration Bee --- Unit {order:02d}:\\\\ {meta['title']}}}
\\author{{UK Uni Integration Bee prep\\\\ Yang {meta['section']}}}
\\date{{}}
\\begin{{document}}
\\maketitle
\\section*{{Status}}
Yang concept unit. Tags: {ytex}; techniques: {ttex}.
\\section{{Official anchors}}
\\begin{{itemize}}
\\item Yang Topics Guide 2nd Ed {sec}
(\\texttt{{sources/user/Integration\\_Bee\\_Topics\\_Guide\\_Yang\\_2nd\\_Ed.pdf}}).
\\item Syllabus §1 (\\texttt{{sources/UK\\_University\\_Integration\\_Bee\\_Syllabus.pdf}}).
\\end{{itemize}}
{meta['body']}
\\section{{Drill pointers}}
See \\texttt{{drills.tex}} / \\texttt{{drills.md}}. Feed: \\texttt{{verify/drills\\_unit{order}.json}}.
\\end{{document}}
"""
    )
    items = "\n".join(
        f"  \\item[\\texttt{{{d['id']}}}] $\\displaystyle {d['latex']}$" for d in drills
    )
    (udir / "drills.tex").write_text(
        f"\\documentclass[11pt]{{article}}\\usepackage[margin=1in]{{geometry}}"
        f"\\usepackage{{amsmath,amssymb}}\\title{{Unit {order:02d} drills}}"
        f"\\begin{{document}}\\maketitle\\begin{{enumerate}}\n{items}\n"
        f"\\end{{enumerate}}\\end{{document}}\n"
    )
    sols = "\n".join(
        f"  \\item \\texttt{{{d['id']}}}: ${d['answer_display']}$" for d in drills
    )
    (udir / "solutions.tex").write_text(
        f"\\documentclass[11pt]{{article}}\\usepackage[margin=1in]{{geometry}}"
        f"\\usepackage{{amsmath,amssymb}}\\title{{Unit {order:02d} solutions}}"
        f"\\begin{{document}}\\maketitle\\begin{{itemize}}\n{sols}\n"
        f"\\end{{itemize}}\\end{{document}}\n"
    )
    rows = [
        "| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for d in drills:
        lim = str(d.get("limits", "")).replace("'", "") if d["kind"] == "definite" else ""
        rows.append(
            f"| {d['id']} | {d['technique']} | {','.join(d['yang'])} | {d['kind']} | "
            f"`{d['sympy_expr']}` | {lim} | `{d['answer_sympy']}` | ${d['answer_display']}$ |"
        )
    (udir / "drills.md").write_text(
        f"# Unit {order:02d} — drill feed\n\nMachine: `../../verify/drills_unit{order}.json`.\n\n"
        + "\n".join(rows) + "\n"
    )
    (udir / "teaching.md").write_text(
        f"# Unit {order:02d} — {meta['title']}\n\nSee `teaching.tex`.\n"
    )
    (udir / "solutions.md").write_text(
        f"# Unit {order:02d} solutions\n\n"
        + "\n".join(f"- `{d['id']}`: ${d['answer_display']}$" for d in drills)
        + "\n"
    )
    # strip hint from machine json? keep solution_note; drop hint key for cleanliness
    out = []
    for d in drills:
        o = {k: v for k, v in d.items() if k != "hint"}
        out.append(o)
    (VERIFY / f"drills_unit{order}.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"OK {uid} ({len(drills)} drills)", flush=True)
    return len(drills)


def try_mk(*a, **k):
    try:
        return mk(*a, **k)
    except Exception as e:
        print(f"DROP {a[0]}: {e}", flush=True)
        return None


def keep(drills):
    return [d for d in drills if d is not None]


def build_all():
    _retired()
    log_rows = []
    specs = []

    def add(uid, title, order, yang, tech, section, prereq, body, drills):
        drills = keep(drills)
        if len(drills) < 4:
            raise RuntimeError(f"{uid}: only {len(drills)} drills survived")
        specs.append(dict(
            uid=uid, title=title, order=order, yang=yang, tech=tech,
            section=section, prereq=prereq, body=body, drills=drills,
        ))
        log_rows.append((uid, order, len(drills), ",".join(yang)))

    # ========== Ch.3 ==========
    add("19-power-sneaky-usub", "Power Substitution and Sneaky U-Sub Tricks", 19,
        ["yang:3.1", "yang:3.2"], ["power-substitution", "sneaky-u-sub"],
        "§§3.1 Power Substitution, 3.2 Sneaky U-Sub Tricks",
        ["06-intermediate-u-sub", "13-forced-u-sub"],
        r"\section{Learning goals} Clear radicals via $u^n=x$; blind/British subs.",
        [
            try_mk("U19-D01", "power-substitution", "yang:3.1", "definite",
                   r"\int_{0}^{1}\frac{1}{1+\sqrt{x}}\,dx", "1/(1+sqrt(x))", "u=√x.",
                   [0, 1], "2-2*log(2)"),
            try_mk("U19-D02", "power-substitution", "yang:3.1", "definite",
                   r"\int_{0}^{1}\frac{1}{1+x^{1/3}}\,dx", "1/(1+x**(Rational(1,3)))",
                   "u=1+x^{1/3}.", [0, 1], "-Rational(3,2)+log(8)"),
            try_mk("U19-D03", "power-substitution", "yang:3.1", "definite",
                   r"\int_{0}^{1}\frac{\sqrt{x}}{1+\sqrt{x}}\,dx", "sqrt(x)/(1+sqrt(x))",
                   "u=√x.", [0, 1], "-1+log(4)"),
            try_mk("U19-D04", "power-substitution", "yang:3.1", "definite",
                   r"\int_{1}^{64}\frac{1}{\sqrt{x}+x^{1/3}}\,dx",
                   "1/(sqrt(x)+x**(Rational(1,3)))", "u^6=x.", [1, 64], "11+log(64/729)"),
            try_mk("U19-D05", "sneaky-u-sub", "yang:3.2", "indefinite",
                   r"\int\frac{1}{(2x+1)\sqrt{x^{2}+x}}\,dx",
                   "1/((2*x+1)*sqrt(x**2+x))", "blind u.", None, "atan(2*sqrt(x**2+x))"),
            try_mk("U19-D06", "sneaky-u-sub", "yang:3.2", "definite",
                   r"\int_{0}^{1}\frac{((x-1)/(x+1))^{3}}{x+1}\,dx",
                   "((x-1)/(x+1))**3/(x+1)", "British.", [0, 1], "-Rational(5,6)+log(2)"),
            try_mk("U19-D07", "sneaky-u-sub", "yang:3.2", "definite",
                   r"\int_{1}^{2}\sqrt{\frac{2-x}{x-1}}\,dx", "sqrt((2-x)/(x-1))",
                   "u².", [1, 2], "pi/2"),
            try_mk("U19-D08", "sneaky-u-sub", "yang:3.2", "definite",
                   r"\int_{0}^{\infty}\frac{1}{1+x^{2}}\,dx", "1/(1+x**2)",
                   "arctan.", [0, "oo"], "pi/2"),
        ])

    add("20-wallis", "Wallis' Trick", 20, ["yang:3.3"], ["wallis"],
        "§3.3 Wallis' Trick", ["02-symmetry-basic-trig", "09-intermediate-trig"],
        r"\section{Learning goals} Wallis on $[0,\pi/2]$.",
        [
            try_mk("U20-D01", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}\cos^{4}x\,dx", "cos(x)**4", "even.", [0, "pi/2"], "3*pi/16"),
            try_mk("U20-D02", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}\sin^{2}x\cos^{2}x\,dx", "sin(x)**2*cos(x)**2",
                   "sin2x.", [0, "pi/2"], "pi/16"),
            try_mk("U20-D03", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}(1+\sin x)^{3}\,dx", "(1+sin(x))**3",
                   "expand.", [0, "pi/2"], "Rational(11,3)+5*pi/4"),
            try_mk("U20-D04", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}\sin^{5}x\,dx", "sin(x)**5", "odd.", [0, "pi/2"], "Rational(8,15)"),
            try_mk("U20-D05", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}\cos^{6}x\,dx", "cos(x)**6", "even.", [0, "pi/2"], "5*pi/32"),
            try_mk("U20-D06", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}\sin^{3}x\cos^{2}x\,dx", "sin(x)**3*cos(x)**2",
                   "u=cos.", [0, "pi/2"], "Rational(2,15)"),
            try_mk("U20-D07", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}\sin^{4}x\,dx", "sin(x)**4", "sym.", [0, "pi/2"], "3*pi/16"),
            try_mk("U20-D08", "wallis", "yang:3.3", "definite",
                   r"\int_{0}^{\pi/2}\cos^{3}x\,dx", "cos(x)**3", "odd cos.", [0, "pi/2"], "Rational(2,3)"),
        ])

    add("21-advanced-trig-sub", "Advanced Trig-Substitution", 21,
        ["yang:3.4"], ["advanced-trig-substitution"],
        "§3.4 Advanced Trig-Substitution", ["04-trig-sub-circle", "09-intermediate-trig"],
        r"\section{Learning goals} Inverse-trig kill; sec/tan on $\sqrt{x^2\pm1}$.",
        [
            try_mk("U21-D01", "advanced-trig-substitution", "yang:3.4", "definite",
                   r"\int_{0}^{1}\frac{\arcsin(2x/(1+x^{2}))}{1+x^{2}}\,dx",
                   "asin(2*x/(1+x**2))/(1+x**2)", "x=tan.", [0, 1], "pi**2/16",
                   verify_mode="numeric"),
            try_mk("U21-D02", "advanced-trig-substitution", "yang:3.4", "definite",
                   r"\int_{0}^{1}\arcsin\sqrt{x/(x+1)}\,dx", "asin(sqrt(x/(x+1)))",
                   "x=tan².", [0, 1], "-1+pi/2"),
            try_mk("U21-D03", "advanced-trig-substitution", "yang:3.4", "definite",
                   r"\int_{1}^{\sqrt{2}}\frac{\sqrt{x^{2}-1}}{x}\,dx", "sqrt(x**2-1)/x",
                   "x=sec.", [1, "sqrt(2)"], "1-pi/4"),
            try_mk("U21-D04", "advanced-trig-substitution", "yang:3.4", "definite",
                   r"\int_{0}^{1}\arctan\sqrt{(1-x)/(1+x)}\,dx", "atan(sqrt((1-x)/(1+x)))",
                   "x=cos2θ.", [0, 1], "Rational(1,2)"),
            try_mk("U21-D05", "advanced-trig-substitution", "yang:3.4", "indefinite",
                   r"\int\frac{1}{\sqrt{x^{2}+1}}\,dx", "1/sqrt(x**2+1)", "asinh.",
                   None, "log(x+sqrt(x**2+1))"),
            try_mk("U21-D06", "advanced-trig-substitution", "yang:3.4", "definite",
                   r"\int_{1}^{\sqrt{2}}\frac{\sqrt{x^{2}-1}}{x^{2}}\,dx", "sqrt(x**2-1)/x**2",
                   "sec.", [1, "sqrt(2)"], "-sqrt(2)/2+log(1+sqrt(2))"),
            try_mk("U21-D07", "advanced-trig-substitution", "yang:3.4", "definite",
                   r"\int_{1}^{\sqrt{2}}\sqrt{x^{2}-1}\,dx", "sqrt(x**2-1)", "sec.",
                   [1, "sqrt(2)"], "-log(1+sqrt(2))/2+sqrt(2)/2"),
            try_mk("U21-D08", "advanced-trig-substitution", "yang:3.4", "definite",
                   r"\int_{0}^{1}\frac{x^{2}}{\sqrt{1-x^{2}}}\,dx", "x**2/sqrt(1-x**2)",
                   "x=sin.", [0, 1], "pi/4"),
        ])

    add("22-awkward-parts-pf", "Awkward Parts and Intermediate Partial Fractions", 22,
        ["yang:3.5", "yang:3.6"], ["awkward-parts", "intermediate-partial-fractions"],
        "§§3.5 Awkward & Advanced Parts, 3.6 Intermediate Partial Fractions",
        ["03-exponential-parts", "05-partial-fractions", "15-parts-regular"],
        r"\section{Learning goals} Parts on $\ln^n$, arctan; intermediate PF.",
        [
            try_mk("U22-D01", "awkward-parts", "yang:3.5", "indefinite",
                   r"\int(\ln x)^{2}\,dx", "log(x)**2", "parts.", None,
                   "x*log(x)**2-2*x*log(x)+2*x"),
            try_mk("U22-D02", "awkward-parts", "yang:3.5", "indefinite",
                   r"\int\arctan x\,dx", "atan(x)", "parts.", None,
                   "x*atan(x)-log(1+x**2)/2"),
            try_mk("U22-D03", "awkward-parts", "yang:3.5", "indefinite",
                   r"\int x^{2}e^{x}\,dx", "x**2*exp(x)", "tabular.", None,
                   "exp(x)*(x**2-2*x+2)"),
            try_mk("U22-D04", "awkward-parts", "yang:3.5", "indefinite",
                   r"\int\arcsin x\,dx", "asin(x)", "parts.", None,
                   "x*asin(x)+sqrt(1-x**2)"),
            try_mk("U22-D05", "awkward-parts", "yang:3.5", "indefinite",
                   r"\int e^{x}\sin x\,dx", "exp(x)*sin(x)", "parts×2.", None,
                   "exp(x)*(sin(x)-cos(x))/2"),
            try_mk("U22-D06", "intermediate-partial-fractions", "yang:3.6", "indefinite",
                   r"\int\frac{x}{(x+1)(x+2)(x+3)}\,dx", "x/((x+1)*(x+2)*(x+3))",
                   "cover-up.", None, "-log(x+1)/2+2*log(x+2)-3*log(x+3)/2"),
            try_mk("U22-D07", "intermediate-partial-fractions", "yang:3.6", "indefinite",
                   r"\int\frac{1}{x^{2}(x+1)}\,dx", "1/(x**2*(x+1))", "PF.", None,
                   "-1/x-log(x)+log(x+1)"),
            try_mk("U22-D08", "intermediate-partial-fractions", "yang:3.6", "definite",
                   r"\int_{1}^{2}\frac{1}{x^{2}(x+1)}\,dx", "1/(x**2*(x+1))",
                   "eval.", [1, 2], "Rational(1,2)+log(Rational(3,4))"),
        ])

    add("23-periodicity-speed", "Basic Periodicity and Speed Bashing", 23,
        ["yang:3.7", "yang:3.8"], ["periodicity", "speed-bashing"],
        "§§3.7 Basic Periodicity, 3.8 Speed Bashing",
        ["02-symmetry-basic-trig", "16-trig-id-trig-sub"],
        r"\section{Learning goals} Orthogonality; watch squares; speed patterns.",
        [
            try_mk("U23-D01", "periodicity", "yang:3.7", "definite",
                   r"\int_{0}^{2\pi}\sin(3x)\sin(5x)\,dx", "sin(3*x)*sin(5*x)",
                   "m≠n.", [0, "2*pi"], "0"),
            try_mk("U23-D02", "periodicity", "yang:3.7", "definite",
                   r"\int_{0}^{2\pi}(\sin x+\sin 2x+\sin 3x)^{2}\,dx",
                   "(sin(x)+sin(2*x)+sin(3*x))**2", "squares.", [0, "2*pi"], "3*pi"),
            try_mk("U23-D03", "periodicity", "yang:3.7", "definite",
                   r"\int_{0}^{\pi}\sin(23x)\sin(19x)\,dx", "sin(23*x)*sin(19*x)",
                   "product.", [0, "pi"], "0"),
            try_mk("U23-D04", "periodicity", "yang:3.7", "definite",
                   r"\int_{0}^{2\pi}20\sin^{2}x\,dx", "20*sin(x)**2",
                   "watch squares.", [0, "2*pi"], "20*pi"),
            try_mk("U23-D05", "periodicity", "yang:3.7", "definite",
                   r"\int_{0}^{2\pi}\cos(3x)\cos(5x)\,dx", "cos(3*x)*cos(5*x)",
                   "m≠n.", [0, "2*pi"], "0"),
            try_mk("U23-D06", "speed-bashing", "yang:3.8", "indefinite",
                   r"\int x^{3}e^{x}\,dx", "x**3*exp(x)", "tabular.", None,
                   "exp(x)*(x**3-3*x**2+6*x-6)"),
            try_mk("U23-D07", "speed-bashing", "yang:3.8", "indefinite",
                   r"\int(\sin^{3}x+\cos^{3}x)\,dx", "sin(x)**3+cos(x)**3", "factor.",
                   None, "-cos(x)+cos(x)**3/3+sin(x)-sin(x)**3/3"),
            try_mk("U23-D08", "speed-bashing", "yang:3.8", "indefinite",
                   r"\int(x^{-2}+x^{-1}+1-(x^{2}+1)^{-1})\,dx",
                   "1/x**2+1/x+1-1/(x**2+1)", "algebra.", None,
                   "-1/x+log(x)+x-atan(x)"),
        ])

    # ========== Ch.4 (skip 4.3) ==========
    add("24-undertow-square", "Undertow and Square-Square", 24,
        ["yang:4.1", "yang:4.2"], ["undertow", "square-square"],
        "§§4.1 Undertow, 4.2 Square-Square (inventory skips 4.3)",
        ["06-intermediate-u-sub", "18-sneaky-symmetry-product"],
        r"\section{Learning goals} Undertow ÷$x$; denest square-square.",
        [
            try_mk("U24-D01", "undertow", "yang:4.1", "indefinite",
                   r"\int\frac{2x^{3}-1}{x^{4}+x}\,dx", "(2*x**3-1)/(x**4+x)",
                   "÷x.", None, "log(x**2+1/x)"),
            try_mk("U24-D02", "undertow", "yang:4.1", "indefinite",
                   r"\int\frac{4x^{5}-1}{(x^{5}+x+1)^{2}}\,dx",
                   "(4*x**5-1)/(x**5+x+1)**2", "chain.", None, "-x/(x**5+x+1)"),
            try_mk("U24-D03", "undertow", "yang:4.1", "indefinite",
                   r"\int\frac{e^{x}-\sin x}{e^{x}+\cos x}\,dx",
                   "(exp(x)-sin(x))/(exp(x)+cos(x))", "num=denom'.", None,
                   "log(exp(x)+cos(x))"),
            try_mk("U24-D04", "undertow", "yang:4.1", "indefinite",
                   r"\int\frac{x^{2}-1}{x^{3}+x}\,dx", "(x**2-1)/(x**3+x)",
                   "÷x.", None, "log(x+1/x)"),
            try_mk("U24-D05", "square-square", "yang:4.2", "indefinite",
                   r"\int(\sqrt{x}+1/\sqrt{x})\,dx", "sqrt(x)+1/sqrt(x)", "denest companion.", None,
                   "(2/3)*x**(Rational(3,2))+2*sqrt(x)"),
            try_mk("U24-D06", "square-square", "yang:4.2", "definite",
                   r"\int_{1}^{4}(\sqrt{x}+x^{-1/2})\,dx", "sqrt(x)+1/sqrt(x)",
                   "direct.", [1, 4], "Rational(20,3)"),
            try_mk("U24-D07", "square-square", "yang:4.2", "definite",
                   r"\int_{1}^{4}\sqrt{x+2+1/x}\,dx", "sqrt(x+2+1/x)",
                   "denest.", [1, 4], "Rational(20,3)"),
            try_mk("U24-D08", "square-square", "yang:4.2", "definite",
                   r"\int_{1}^{4}(\sqrt{x}-x^{-1/2})\,dx", "sqrt(x)-1/sqrt(x)",
                   "companion.", [1, 4], "Rational(8,3)"),
        ])

    add("25-advanced-kings", "Advanced King's/Queen's Rule", 25,
        ["yang:4.4"], ["advanced-kings-queens"],
        "§4.4 Advanced King's/Queen's Rule", ["10-inverse-kings"],
        r"\section{Learning goals} $f(a+b-x)$ on nested trig/exp (SymPy-friendly).",
        [
            try_mk("U25-D01", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{\pi/2}\frac{\sin x}{\sin x+\cos x}\,dx",
                   "sin(x)/(sin(x)+cos(x))", "king.", [0, "pi/2"], "pi/4"),
            try_mk("U25-D02", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{\pi/2}\frac{\cos x}{\sin x+\cos x}\,dx",
                   "cos(x)/(sin(x)+cos(x))", "pair.", [0, "pi/2"], "pi/4"),
            try_mk("U25-D03", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{1}\frac{e^{x}}{e^{x}+e^{1-x}}\,dx",
                   "exp(x)/(exp(x)+exp(1-x))", "x→1-x.", [0, 1], "Rational(1,2)"),
            try_mk("U25-D04", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{\pi/4}\frac{1}{1+\tan x}\,dx", "1/(1+tan(x))",
                   "π/4-x; ans π/8+log2/4.", [0, "pi/4"], "pi/8+log(2)/4"),
            # avoid log-king hang; use solvable nested forms
            try_mk("U25-D05", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{\pi/2}\frac{\sin^{3}x}{\sin^{3}x+\cos^{3}x}\,dx",
                   "sin(x)**3/(sin(x)**3+cos(x)**3)", "king.", [0, "pi/2"], "pi/4"),
            try_mk("U25-D06", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{\pi}\frac{x}{1+\sin x}\,dx",
                   "x/(1+sin(x))", "π-x.", [0, "pi"], "pi",
                   ),
            try_mk("U25-D07", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{1}\frac{x}{1+x}\,dx", "x/(1+x)", "warmup.",
                   [0, 1], "1-log(2)"),
            try_mk("U25-D08", "advanced-kings-queens", "yang:4.4", "definite",
                   r"\int_{0}^{\pi/2}\sin x\cos x\,dx", "sin(x)*cos(x)",
                   "u=sin.", [0, "pi/2"], "Rational(1,2)"),
        ])

    add("26-weierstrass", "Weierstrass Substitution", 26,
        ["yang:4.5"], ["weierstrass"],
        "§4.5 Weierstrass Substitution",
        ["05-partial-fractions", "02-symmetry-basic-trig"],
        r"\section{Learning goals} $t=\tan(x/2)$ for rational trig.",
        [
            try_mk("U26-D01", "weierstrass", "yang:4.5", "definite",
                   r"\int_{0}^{\pi/2}\frac{1}{1+\sin x}\,dx", "1/(1+sin(x))",
                   "t-sub.", [0, "pi/2"], "1"),
            try_mk("U26-D02", "weierstrass", "yang:4.5", "definite",
                   r"\int_{0}^{\pi}\frac{1}{2+\cos x}\,dx", "1/(2+cos(x))",
                   "std.", [0, "pi"], "pi/sqrt(3)"),
            try_mk("U26-D03", "weierstrass", "yang:4.5", "definite",
                   r"\int_{0}^{\pi}\frac{1}{3+2\cos x}\,dx", "1/(3+2*cos(x))",
                   "formula.", [0, "pi"], "pi/sqrt(5)"),
            try_mk("U26-D04", "weierstrass", "yang:4.5", "indefinite",
                   r"\int\frac{1}{1+\sin x}\,dx", "1/(1+sin(x))", "t.",
                   None, "tan(x)-sec(x)"),
            try_mk("U26-D05", "weierstrass", "yang:4.5", "definite",
                   r"\int_{0}^{\pi}\frac{1}{5+4\cos x}\,dx", "1/(5+4*cos(x))",
                   "a=5.", [0, "pi"], "pi/3"),
            try_mk("U26-D06", "weierstrass", "yang:4.5", "definite",
                   r"\int_{0}^{\pi/2}\frac{1}{1+\cos x+\sin x}\,dx",
                   "1/(1+cos(x)+sin(x))", "wei.", [0, "pi/2"], "log(2)"),
            try_mk("U26-D07", "weierstrass", "yang:4.5", "definite",
                   r"\int_{0}^{\pi/3}\frac{1}{2+\cos x}\,dx", "1/(2+cos(x))",
                   "scaled.", [0, "pi/3"], "2*sqrt(3)*atan(Rational(1,3))/3"),
            try_mk("U26-D08", "weierstrass", "yang:4.5", "definite",
                   r"\int_{0}^{\pi/2}\frac{1}{2+\sin x}\,dx", "1/(2+sin(x))",
                   "wei.", [0, "pi/2"], "sqrt(3)*pi/9"),
        ])

    add("27-reverse-quotient", "Reverse Quotient Rule", 27,
        ["yang:4.6"], ["reverse-quotient"],
        "§4.6 Reverse Quotient Rule",
        ["07-abs-reverse-product", "18-sneaky-symmetry-product"],
        r"\section{Learning goals} Spot $(f'g-fg')/g^2\to f/g$.",
        [
            try_mk("U27-D01", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{x\cos x-\sin x}{x^{2}}\,dx",
                   "(x*cos(x)-sin(x))/x**2", "sin/x.", None, "sin(x)/x"),
            try_mk("U27-D02", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{e^{x}(x-1)}{x^{2}}\,dx", "exp(x)*(x-1)/x**2",
                   "e^x/x.", None, "exp(x)/x"),
            try_mk("U27-D03", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{1-\ln x}{x^{2}}\,dx", "(1-log(x))/x**2",
                   "ln/x.", None, "log(x)/x"),
            try_mk("U27-D04", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{\sin x-x\cos x}{\sin^{2}x}\,dx",
                   "(sin(x)-x*cos(x))/sin(x)**2", "x/sin.", None, "x/sin(x)"),
            try_mk("U27-D05", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{\ln x-1}{x^{2}}\,dx", "(log(x)-1)/x**2",
                   "sign twin.", None, "-log(x)/x"),
            try_mk("U27-D06", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{(x+1)e^{x}-e^{x}}{(x+1)^{2}}\,dx",
                   "((x+1)*exp(x)-exp(x))/(x+1)**2", "e^x/(x+1).", None,
                   "exp(x)/(x+1)"),
            try_mk("U27-D07", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{x\sec^{2}x-\tan x}{x^{2}}\,dx",
                   "(x*sec(x)**2-tan(x))/x**2", "tan/x.", None, "tan(x)/x"),
            try_mk("U27-D08", "reverse-quotient", "yang:4.6", "indefinite",
                   r"\int\frac{x^{2}\cos x-2x\sin x}{x^{4}}\,dx",
                   "(x**2*cos(x)-2*x*sin(x))/x**4", "sin/x².", None, "sin(x)/x**2"),
        ])

    # ========== Ch.5 ==========
    add("28-semi-parts", "Semi-Integration by Parts", 28,
        ["yang:5.1"], ["semi-parts"],
        "§5.1 Semi-Integration by Parts", ["15-parts-regular", "22-awkward-parts-pf"],
        r"\section{Learning goals} Semi-parts / tabular shortcuts.",
        [
            try_mk("U28-D01", "semi-parts", "yang:5.1", "indefinite",
                   r"\int x e^{x}\,dx", "x*exp(x)", "semi.", None, "exp(x)*(x-1)"),
            try_mk("U28-D02", "semi-parts", "yang:5.1", "indefinite",
                   r"\int x\sin x\,dx", "x*sin(x)", "parts.", None, "-x*cos(x)+sin(x)"),
            try_mk("U28-D03", "semi-parts", "yang:5.1", "indefinite",
                   r"\int x\cos x\,dx", "x*cos(x)", "parts.", None, "x*sin(x)+cos(x)"),
            try_mk("U28-D04", "semi-parts", "yang:5.1", "indefinite",
                   r"\int x\ln x\,dx", "x*log(x)", "parts.", None,
                   "x**2*log(x)/2-x**2/4"),
            try_mk("U28-D05", "semi-parts", "yang:5.1", "definite",
                   r"\int_{0}^{\pi}e^{x}\sin x\,dx", "exp(x)*sin(x)", "parts×2.",
                   [0, "pi"], "(1+exp(pi))/2"),
            try_mk("U28-D06", "semi-parts", "yang:5.1", "indefinite",
                   r"\int\ln x\,dx", "log(x)", "classic.", None, "x*log(x)-x"),
            try_mk("U28-D07", "semi-parts", "yang:5.1", "definite",
                   r"\int_{0}^{1}x e^{x}\,dx", "x*exp(x)", "eval.", [0, 1], "1"),
            try_mk("U28-D08", "semi-parts", "yang:5.1", "indefinite",
                   r"\int x^{2}\sin x\,dx", "x**2*sin(x)", "tabular.", None,
                   "-x**2*cos(x)+2*x*sin(x)+2*cos(x)"),
        ])

    add("29-advanced-trig", "Advanced Trig Integrals", 29,
        ["yang:5.2"], ["advanced-trig-integrals"],
        "§5.2 Advanced Trig Integrals", ["16-trig-id-trig-sub", "20-wallis"],
        r"\section{Learning goals} Higher trig powers/products.",
        [
            try_mk("U29-D01", "advanced-trig-integrals", "yang:5.2", "definite",
                   r"\int_{0}^{\pi/2}\sin^{6}x\,dx", "sin(x)**6", "Wallis.",
                   [0, "pi/2"], "5*pi/32"),
            try_mk("U29-D02", "advanced-trig-integrals", "yang:5.2", "definite",
                   r"\int_{0}^{\pi/4}\tan^{2}x\,dx", "tan(x)**2", "sec²-1.",
                   [0, "pi/4"], "1-pi/4"),
            try_mk("U29-D03", "advanced-trig-integrals", "yang:5.2", "indefinite",
                   r"\int\tan x\sec^{2}x\,dx", "tan(x)*sec(x)**2", "u=tan.",
                   None, "tan(x)**2/2"),
            try_mk("U29-D04", "advanced-trig-integrals", "yang:5.2", "definite",
                   r"\int_{0}^{\pi/2}\sin x\cos^{5}x\,dx", "sin(x)*cos(x)**5",
                   "u=cos.", [0, "pi/2"], "Rational(1,6)"),
            try_mk("U29-D05", "advanced-trig-integrals", "yang:5.2", "definite",
                   r"\int_{0}^{\pi/3}\sec x\,dx", "sec(x)", "std.",
                   [0, "pi/3"], "log(2+sqrt(3))"),
            try_mk("U29-D06", "advanced-trig-integrals", "yang:5.2", "definite",
                   r"\int_{0}^{\pi/2}\cos^{2}x\sin^{4}x\,dx", "cos(x)**2*sin(x)**4",
                   "Wallis product.", [0, "pi/2"], "pi/32"),
            try_mk("U29-D07", "advanced-trig-integrals", "yang:5.2", "indefinite",
                   r"\int\sin(2x)\cos(2x)\,dx", "sin(2*x)*cos(2*x)", "double.",
                   None, "sin(2*x)**2/4"),
            try_mk("U29-D08", "advanced-trig-integrals", "yang:5.2", "definite",
                   r"\int_{0}^{\pi/4}\sec^{2}x\,dx", "sec(x)**2", "tan.",
                   [0, "pi/4"], "1"),
        ])

    add("30-gaussian-dirichlet", "Advanced Gaussian and Dirichlet", 30,
        ["yang:5.3", "yang:5.4"], ["advanced-gaussian", "dirichlet"],
        "§§5.3 Advanced Gaussian, 5.4 Dirichlet Integral",
        ["11-gaussian-wildcard"],
        r"\section{Learning goals} Gaussian variants; Dirichlet $\sin x/x$.",
        [
            try_mk("U30-D01", "advanced-gaussian", "yang:5.3", "definite",
                   r"\int_{0}^{\infty}e^{-x^{2}}\,dx", "exp(-x**2)", "half Gauss.",
                   [0, "oo"], "sqrt(pi)/2"),
            try_mk("U30-D02", "advanced-gaussian", "yang:5.3", "definite",
                   r"\int_{0}^{\infty}x e^{-x^{2}}\,dx", "x*exp(-x**2)", "u=x².",
                   [0, "oo"], "Rational(1,2)"),
            try_mk("U30-D03", "advanced-gaussian", "yang:5.3", "definite",
                   r"\int_{-\infty}^{\infty}e^{-x^{2}}\,dx", "exp(-x**2)", "full.",
                   ["-oo", "oo"], "sqrt(pi)"),
            try_mk("U30-D04", "advanced-gaussian", "yang:5.3", "definite",
                   r"\int_{0}^{\infty}e^{-x^{2}}x^{2}\,dx", "exp(-x**2)*x**2",
                   "Γ related.", [0, "oo"], "sqrt(pi)/4"),
            try_mk("U30-D05", "dirichlet", "yang:5.4", "definite",
                   r"\int_{0}^{\infty}\frac{\sin x}{x}\,dx", "sin(x)/x",
                   "Dirichlet.", [0, "oo"], "pi/2"),
            try_mk("U30-D06", "dirichlet", "yang:5.4", "definite",
                   r"\int_{0}^{\infty}\frac{\sin^{2}x}{x^{2}}\,dx", "sin(x)**2/x**2",
                   "parts/Feynman.", [0, "oo"], "pi/2"),
            try_mk("U30-D07", "dirichlet", "yang:5.4", "definite",
                   r"\int_{0}^{\infty}e^{-x}\sin x\,dx", "exp(-x)*sin(x)",
                   "Im Laplace.", [0, "oo"], "Rational(1,2)"),
            try_mk("U30-D08", "dirichlet", "yang:5.4", "definite",
                   r"\int_{0}^{\infty}e^{-x}\cos x\,dx", "exp(-x)*cos(x)",
                   "Re Laplace.", [0, "oo"], "Rational(1,2)"),
        ])

    # ========== Ch.6 ==========
    add("31-inverse-jailbreak", "Inverse Jailbreaking", 31,
        ["yang:6.1"], ["inverse-jailbreaking"],
        "§6.1 Inverse Jailbreaking", ["10-inverse-kings", "28-semi-parts"],
        r"\section{Learning goals} Integrate inverses by parts / geometry.",
        [
            try_mk("U31-D01", "inverse-jailbreaking", "yang:6.1", "definite",
                   r"\int_{0}^{1}\arcsin x\,dx", "asin(x)", "parts/geo.",
                   [0, 1], "-1+pi/2"),
            try_mk("U31-D02", "inverse-jailbreaking", "yang:6.1", "definite",
                   r"\int_{0}^{1}\arctan x\,dx", "atan(x)", "parts.",
                   [0, 1], "pi/4-log(2)/2"),
            try_mk("U31-D03", "inverse-jailbreaking", "yang:6.1", "definite",
                   r"\int_{0}^{1}\arccos x\,dx", "acos(x)", "parts.", [0, 1], "1"),
            try_mk("U31-D04", "inverse-jailbreaking", "yang:6.1", "indefinite",
                   r"\int\arctan x\,dx", "atan(x)", "parts.", None,
                   "x*atan(x)-log(1+x**2)/2"),
            try_mk("U31-D05", "inverse-jailbreaking", "yang:6.1", "definite",
                   r"\int_{0}^{1/2}\arcsin x\,dx", "asin(x)", "eval.",
                   [0, "Rational(1,2)"], "-1+pi/12+sqrt(3)/2"),
            try_mk("U31-D06", "inverse-jailbreaking", "yang:6.1", "indefinite",
                   r"\int x\arctan x\,dx", "x*atan(x)", "parts.", None,
                   "(x**2+1)*atan(x)/2-x/2"),
            try_mk("U31-D07", "inverse-jailbreaking", "yang:6.1", "definite",
                   r"\int_{0}^{1}x\arcsin x\,dx", "x*asin(x)", "parts.",
                   [0, 1], "pi/8"),  # may need recovery
            try_mk("U31-D08", "inverse-jailbreaking", "yang:6.1", "indefinite",
                   r"\int\arcsin x\,dx", "asin(x)", "parts.", None,
                   "x*asin(x)+sqrt(1-x**2)"),
        ])

    add("32-taylor-complex", "Taylor Series and Complexifying", 32,
        ["yang:6.2", "yang:6.3"], ["taylor-series", "complexifying"],
        "§§6.2 Taylor Series, 6.3 Complexifying the Integral",
        ["08-basic-series", "03-exponential-parts"],
        r"\section{Learning goals} Termwise Taylor; $\mathrm{Re}/\mathrm{Im}\,e^{ix}$.",
        [
            try_mk("U32-D01", "taylor-series", "yang:6.2", "definite",
                   r"\int_{0}^{1}\frac{1}{1+x}\,dx", "1/(1+x)", "geom series.",
                   [0, 1], "log(2)"),
            try_mk("U32-D02", "taylor-series", "yang:6.2", "definite",
                   r"\int_{0}^{1}\sum_{n=0}^{3}\frac{(-1)^{n}}{n!}x^{2n}\,dx".replace(
                       r"\sum_{n=0}^{3}\frac{(-1)^{n}}{n!}x^{2n}",
                       r"1-x^{2}+x^{4}/2-x^{6}/6"),
                   "1-x**2+x**4/2-x**6/6", "Taylor truncate.",
                   [0, 1], "1-Rational(1,3)+Rational(1,10)-Rational(1,42)"),
            try_mk("U32-D03", "taylor-series", "yang:6.2", "indefinite",
                   r"\int e^{x^{2}}x\,dx", "x*exp(x**2)", "series/u.", None,
                   "exp(x**2)/2"),
            try_mk("U32-D04", "taylor-series", "yang:6.2", "definite",
                   r"\int_{0}^{1}x^{3}\,dx", "x**3", "warmup term.", [0, 1],
                   "Rational(1,4)"),
            try_mk("U32-D05", "complexifying", "yang:6.3", "definite",
                   r"\int_{0}^{\infty}e^{-x}\cos x\,dx", "exp(-x)*cos(x)",
                   "Re e^{-(1-i)x}.", [0, "oo"], "Rational(1,2)"),
            try_mk("U32-D06", "complexifying", "yang:6.3", "definite",
                   r"\int_{0}^{\infty}e^{-x}\sin x\,dx", "exp(-x)*sin(x)",
                   "Im.", [0, "oo"], "Rational(1,2)"),
            try_mk("U32-D07", "complexifying", "yang:6.3", "indefinite",
                   r"\int e^{x}\cos x\,dx", "exp(x)*cos(x)", "Re e^{(1+i)x}.",
                   None, "exp(x)*(cos(x)+sin(x))/2"),
            try_mk("U32-D08", "complexifying", "yang:6.3", "indefinite",
                   r"\int e^{x}\sin x\,dx", "exp(x)*sin(x)", "Im.",
                   None, "exp(x)*(sin(x)-cos(x))/2"),
        ])

    # Fix U32-D02: need closed form sympy knows — use erf or skip
    # We'll recompute after; for now leave and let try_mk with ans from integrate

    add("33-ninja-inversion", "Ninja Substitution and Inversion", 33,
        ["yang:6.4", "yang:6.5"], ["ninja-substitution", "inversion"],
        "§§6.4 Ninja Substitution, 6.5 Inversion",
        ["13-forced-u-sub", "18-sneaky-symmetry-product"],
        r"\section{Learning goals} Clever $u$; $x\mapsto 1/x$ inversion.",
        [
            try_mk("U33-D01", "ninja-substitution", "yang:6.4", "definite",
                   r"\int_{0}^{1}\frac{x}{1+x^{2}}\,dx", "x/(1+x**2)", "u=1+x².",
                   [0, 1], "log(2)/2"),
            try_mk("U33-D02", "ninja-substitution", "yang:6.4", "definite",
                   r"\int_{0}^{\pi/2}\frac{1}{1+\sin^{2}x}\,dx", "1/(1+sin(x)**2)",
                   "ninja/t.", [0, "pi/2"], "pi/(2*sqrt(2))",
                   verify_mode="numeric"),
            try_mk("U33-D03", "ninja-substitution", "yang:6.4", "indefinite",
                   r"\int\frac{1}{x\sqrt{x^{2}-1}}\,dx", "1/(x*sqrt(x**2-1))",
                   "sec/ninja.", None, "atan(sqrt(x**2-1))"),  # or asec
            try_mk("U33-D04", "ninja-substitution", "yang:6.4", "definite",
                   r"\int_{0}^{1}\frac{\ln(1+x)}{1+x^{2}}\,dx", "log(1+x)/(1+x**2)",
                   "ninja.", [0, 1], "pi*log(2)/8",
                   verify_mode="numeric"),
            try_mk("U33-D05", "inversion", "yang:6.5", "definite",
                   r"\int_{0}^{\infty}\frac{1}{1+x^{2}}\,dx", "1/(1+x**2)",
                   "x→1/x same.", [0, "oo"], "pi/2"),
            try_mk("U33-D06", "inversion", "yang:6.5", "definite",
                   r"\int_{0}^{\infty}\frac{1}{(1+x^{2})(1+x)}\,dx",
                   "1/((1+x**2)*(1+x))", "x→1/x.", [0, "oo"], "pi/4",
                   verify_mode="numeric"),
            try_mk("U33-D07", "inversion", "yang:6.5", "definite",
                   r"\int_{0}^{\infty}\frac{\ln x}{1+x^{2}}\,dx", "log(x)/(1+x**2)",
                   "x→1/x ⇒0.", [0, "oo"], "0"),
            try_mk("U33-D08", "inversion", "yang:6.5", "definite",
                   r"\int_{0}^{\infty}\frac{x}{(1+x^{2})^{2}}\,dx", "x/(1+x**2)**2",
                   "u=1+x².", [0, "oo"], "Rational(1,2)"),
        ])

    add("34-frullani-feynman", "Frullani Integrals and Feynman Technique", 34,
        ["yang:6.6", "yang:6.7"], ["frullani", "feynman"],
        "§§6.6 Frullani Integrals, 6.7 Feynman Technique",
        ["30-gaussian-dirichlet", "17-infinite-functions"],
        r"\section{Learning goals} Frullani template; differentiate under integral.",
        [
            try_mk("U34-D01", "frullani", "yang:6.6", "definite",
                   r"\int_{0}^{\infty}\frac{e^{-ax}-e^{-bx}}{x}\,dx",
                   # use a=1,b=2 concrete
                   "(exp(-x)-exp(-2*x))/x", "Frullani ln(b/a).",
                   [0, "oo"], "log(2)"),
            try_mk("U34-D02", "frullani", "yang:6.6", "definite",
                   r"\int_{0}^{\infty}\frac{e^{-x}-e^{-3x}}{x}\,dx",
                   "(exp(-x)-exp(-3*x))/x", "Frullani.", [0, "oo"], "log(3)"),
            try_mk("U34-D03", "frullani", "yang:6.6", "definite",
                   r"\int_{0}^{\infty}\frac{\cos x-\cos(2x)}{x}\,dx",
                   "(cos(x)-cos(2*x))/x", "Frullani trig.", [0, "oo"], "log(2)"),
            try_mk("U34-D04", "feynman", "yang:6.7", "definite",
                   r"\int_{0}^{1}\frac{x^{a}-1}{\ln x}\,dx",  # a=2 concrete
                   "(x**2-1)/log(x)", "Feynman I(a).", [0, 1], "log(3)"),  # I(2)=ln3? wait I(a)=ln(a+1), I(2)=ln3
            try_mk("U34-D05", "feynman", "yang:6.7", "definite",
                   r"\int_{0}^{1}x^{2}\ln x\,dx", "x**2*log(x)", "param.",
                   [0, 1], "-Rational(1,9)"),
            try_mk("U34-D06", "feynman", "yang:6.7", "definite",
                   r"\int_{0}^{\infty}e^{-ax}\sin x\,dx",  # a=1
                   "exp(-x)*sin(x)", "I(a).", [0, "oo"], "Rational(1,2)"),
            try_mk("U34-D07", "feynman", "yang:6.7", "definite",
                   r"\int_{0}^{1}\frac{\ln(1+x)}{1+x}\,dx", "log(1+x)/(1+x)",
                   "u=1+x.", [0, 1], "log(2)**2/2"),
            try_mk("U34-D08", "feynman", "yang:6.7", "definite",
                   r"\int_{0}^{\infty}x e^{-x}\,dx", "x*exp(-x)", "Γ'.",
                   [0, "oo"], "1"),
        ])

    add("35-modified-famous", "Modified Famous Integrals", 35,
        ["yang:6.8"], ["modified-famous"],
        "§6.8 Modified Famous Integrals",
        ["30-gaussian-dirichlet", "14-gamma"],
        r"\section{Learning goals} Tweaks of classic integrals.",
        [
            try_mk("U35-D01", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{\infty}e^{-2x^{2}}\,dx", "exp(-2*x**2)",
                   "scaled Gauss.", [0, "oo"], "sqrt(2)*sqrt(pi)/4"),
            try_mk("U35-D02", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{\infty}\frac{\sin(2x)}{x}\,dx", "sin(2*x)/x",
                   "Dirichlet scale.", [0, "oo"], "pi/2"),
            try_mk("U35-D03", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{\infty}e^{-3x}\,dx", "exp(-3*x)", "Γ scale.",
                   [0, "oo"], "Rational(1,3)"),
            try_mk("U35-D04", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{1}\frac{\ln x}{1-x}\,dx", "log(x)/(1-x)",
                   "-ζ(2).", [0, 1], "-pi**2/6"),
            try_mk("U35-D05", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{1}\frac{\ln x}{1+x}\,dx", "log(x)/(1+x)",
                   "-π²/12.", [0, 1], "-pi**2/12",
                   verify_mode="numeric"),
            try_mk("U35-D06", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{\pi/2}\ln(\sin x)\,dx", "log(sin(x))",
                   "famous.", [0, "pi/2"], "-pi*log(2)/2",
                   verify_mode="numeric"),
            try_mk("U35-D07", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{\infty}\frac{e^{-x}-e^{-2x}}{x}\,dx",
                   "(exp(-x)-exp(-2*x))/x", "Frullani-famous.", [0, "oo"], "log(2)"),
            try_mk("U35-D08", "modified-famous", "yang:6.8", "definite",
                   r"\int_{0}^{1}(-\ln x)\,dx", "-log(x)", "Γ(2).", [0, 1], "1"),
        ])

    add("36-unique-tricks", "Unique Tricks", 36,
        ["yang:6.9"], ["unique-tricks"],
        "§6.9 Unique Tricks",
        ["23-periodicity-speed", "33-ninja-inversion"],
        r"\section{Learning goals} One-off contest tricks (SymPy-checkable).",
        [
            try_mk("U36-D01", "unique-tricks", "yang:6.9", "definite",
                   r"\int_{0}^{1}\frac{x-1}{\ln x}\,dx", "(x-1)/log(x)",
                   "sophomore-adjacent.", [0, 1], "log(2)"),
            try_mk("U36-D02", "unique-tricks", "yang:6.9", "definite",
                   r"\int_{0}^{\pi/2}\ln(\sin x)\,dx", "log(sin(x))",
                   "famous twin.", [0, "pi/2"], "-pi*log(2)/2",
                   verify_mode="numeric"),
            try_mk("U36-D03", "unique-tricks", "yang:6.9", "definite",
                   r"\int_{0}^{1}\frac{\arctan x}{x}\,dx", "atan(x)/x",
                   "Catalan.", [0, 1], "Catalan",
                   verify_mode="numeric"),
            try_mk("U36-D04", "unique-tricks", "yang:6.9", "indefinite",
                   r"\int\frac{1}{x\ln x}\,dx", "1/(x*log(x))", "u=lnx.",
                   None, "log(log(x))"),
            try_mk("U36-D05", "unique-tricks", "yang:6.9", "definite",
                   r"\int_{2}^{4}\frac{1}{x\ln x}\,dx", "1/(x*log(x))",
                   "u=ln.", [2, 4], "log(2)"),
            try_mk("U36-D06", "unique-tricks", "yang:6.9", "definite",
                   r"\int_{e}^{e^{e}}\frac{1}{x\ln x}\,dx", "1/(x*log(x))",
                   "u=ln x → ln|ln x|.", ["E", "exp(E)"], "1"),
            try_mk("U36-D07", "unique-tricks", "yang:6.9", "definite",
                   r"\int_{0}^{1}\frac{x^{2}-1}{\ln x}\,dx", "(x**2-1)/log(x)",
                   "Feynman twin.", [0, 1], "log(3)"),
            try_mk("U36-D08", "unique-tricks", "yang:6.9", "indefinite",
                   r"\int\frac{\ln x}{x}\,dx", "log(x)/x", "u=ln.",
                   None, "log(x)**2/2"),
        ])

    # Unit 37 buffer if needed for leftover 6.x — optional merge already done
    return specs, log_rows


def update_indexes(specs, log_rows):
    _retired()
    # units README
    readme = UNITS / "README.md"
    text = readme.read_text()
    # append rows before the closing note if not present
    rows = []
    for s in specs:
        yang = ", ".join(y.replace("yang:", "") for y in s["yang"])
        rows.append(
            f"| `{s['uid']}/` | {s['title']} | {yang} | ready |"
        )
    block = "\n".join(rows)
    if "19-power-sneaky-usub" not in text:
        text = text.replace(
            "Yang Ch.1 (01–11) and Ch.2 (12–18) concept units complete.",
            block + "\n\nYang Ch.1–6 concept units through 6.9 complete.",
        )
        # also insert table rows before Ch.1 note — find last table row
        marker = "| `18-sneaky-symmetry-product/` |"
        if marker in text:
            # insert after unit 18 row
            lines = text.splitlines()
            out = []
            for ln in lines:
                out.append(ln)
                if ln.startswith(marker):
                    out.extend(rows)
            text = "\n".join(out) + ("\n" if not text.endswith("\n") else "")
        readme.write_text(text)

    # skill-tree
    st = ROOT / "skill-tree.md"
    st_text = st.read_text()
    if "yang:3.1" not in st_text and "power-substitution" not in st_text:
        ch_block = ["\n## Yang Ch.3–6 (complete)\n",
                    "| Node | Yang | Unit | Status in curriculum |",
                    "|---|---|---|---|"]
        node_map = [
            ("power-substitution", "3.1", "19-power-sneaky-usub"),
            ("sneaky-u-sub", "3.2", "19-power-sneaky-usub"),
            ("wallis", "3.3", "20-wallis"),
            ("advanced-trig-substitution", "3.4", "21-advanced-trig-sub"),
            ("awkward-parts", "3.5", "22-awkward-parts-pf"),
            ("intermediate-partial-fractions", "3.6", "22-awkward-parts-pf"),
            ("periodicity", "3.7", "23-periodicity-speed"),
            ("speed-bashing", "3.8", "23-periodicity-speed"),
            ("undertow", "4.1", "24-undertow-square"),
            ("square-square", "4.2", "24-undertow-square"),
            ("advanced-kings-queens", "4.4", "25-advanced-kings"),
            ("weierstrass", "4.5", "26-weierstrass"),
            ("reverse-quotient", "4.6", "27-reverse-quotient"),
            ("semi-parts", "5.1", "28-semi-parts"),
            ("advanced-trig-integrals", "5.2", "29-advanced-trig"),
            ("advanced-gaussian", "5.3", "30-gaussian-dirichlet"),
            ("dirichlet", "5.4", "30-gaussian-dirichlet"),
            ("inverse-jailbreaking", "6.1", "31-inverse-jailbreak"),
            ("taylor-series", "6.2", "32-taylor-complex"),
            ("complexifying", "6.3", "32-taylor-complex"),
            ("ninja-substitution", "6.4", "33-ninja-inversion"),
            ("inversion", "6.5", "33-ninja-inversion"),
            ("frullani", "6.6", "34-frullani-feynman"),
            ("feynman", "6.7", "34-frullani-feynman"),
            ("modified-famous", "6.8", "35-modified-famous"),
            ("unique-tricks", "6.9", "36-unique-tricks"),
        ]
        for n, y, u in node_map:
            ch_block.append(f"| {n} | {y} | {u} | content ready |")
        ch_block.append("\n**Still deferred:** none for Yang inventory 3.1–6.9 (4.3 skipped by inventory).\n")
        st_text = st_text.replace(
            "**Still deferred:** Yang Ch.3+ — see `sources/user/yang-topics-inventory.md`.",
            "\n".join(ch_block),
        )
        st.write_text(st_text)

    # syllabus-map: append Ch.3–6 section
    sm = ROOT / "syllabus-map.md"
    sm_text = sm.read_text()
    if "yang:3.1" not in sm_text.split("Yang Chapter 3")[-1] if "Yang Chapter 3" in sm_text else True:
        if "## Yang Chapter 3" not in sm_text and "| `yang:3.1`" not in sm_text:
            table = [
                "\n---\n\n## Yang Chapters 3–6 — full 3.1–6.9 (skip inventory 4.3)\n",
                "| yang id | Topic | Unit status |",
                "|---|---|---|",
            ]
            inv = {
                "3.1": ("Power Substitution", "19"),
                "3.2": ("Sneaky U-Sub Tricks", "19"),
                "3.3": ("Wallis' Trick", "20"),
                "3.4": ("Advanced Trig-Substitution", "21"),
                "3.5": ("Awkward & Advanced Parts", "22"),
                "3.6": ("Intermediate Partial Fractions", "22"),
                "3.7": ("Basic Periodicity", "23"),
                "3.8": ("Speed Bashing", "23"),
                "4.1": ("Undertow Technique", "24"),
                "4.2": ("Square-Square Technique", "24"),
                "4.4": ("Advanced King's/Queen's Rule", "25"),
                "4.5": ("Weierstrass Substitution", "26"),
                "4.6": ("Reverse Quotient Rule", "27"),
                "5.1": ("Semi-Integration by Parts", "28"),
                "5.2": ("Advanced Trig Integrals", "29"),
                "5.3": ("Advanced Gaussian Integral", "30"),
                "5.4": ("Dirichlet Integral", "30"),
                "6.1": ("Inverse Jailbreaking", "31"),
                "6.2": ("Taylor Series", "32"),
                "6.3": ("Complexifying the Integral", "32"),
                "6.4": ("Ninja Substitution", "33"),
                "6.5": ("Inversion", "33"),
                "6.6": ("Frullani Integrals", "34"),
                "6.7": ("Feynman Technique", "34"),
                "6.8": ("Modified Famous Integrals", "35"),
                "6.9": ("Unique Tricks", "36"),
            }
            for yid, (topic, u) in inv.items():
                table.append(f"| `yang:{yid}` | {topic} | **Unit {u}** |")
            table.append("\n**Done:** Units 19–36 cover inventory `yang:3.1`…`yang:6.9` (4.3 skipped).\n")
            sm.write_text(sm_text.rstrip() + "\n" + "\n".join(table) + "\n")

    # STATE
    state = ROOT / "STATE.md"
    stt = state.read_text()
    stt = stt.replace(
        "| next | Yang Ch.3+ | concept | PENDING |",
        "| 19–36 | Yang 3.1…6.9 (skip 4.3) | concept | **DONE** |\n| next | per-Q past tags / deeper mocks | past deep | OPTIONAL |",
    )
    if "YANG_CH3_TO_CH6" not in stt:
        stt = stt.replace(
            "## Status\n",
            "## Status\n\n**`YANG_CH3_TO_CH6_READY`** — 2026-10-24 Asia/Singapore  \n"
            "- Units 19–36 cover Yang inventory 3.1–6.9 (4.3 skipped)  \n"
            "- Concept drills SymPy-checked via `verify/run.sh`  \n\n",
        )
    state.write_text(stt)

    # runlog append
    from datetime import datetime
    # box is Asia/Singapore
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M+08:00")
    n_drills = sum(len(s["drills"]) for s in specs)
    entry = (
        f"\n## {stamp} (Asia/Singapore)\n"
        f"- Yang Ch.3→6.9 units 19–36 written ({len(specs)} units, {n_drills} new drills)\n"
        f"- Updated syllabus-map / skill-tree / STATE / units README\n"
        f"- Gate: ./verify/run.sh\n"
    )
    (ROOT / "runlog.md").write_text((ROOT / "runlog.md").read_text() + entry)

    # audit tsv
    tsv = AUDIT / "yang-ch3.tsv"
    with tsv.open("w") as f:
        f.write("unit\torder\tn_drills\tyang\n")
        for uid, order, n, yang in log_rows:
            f.write(f"{uid}\t{order}\t{n}\t{yang}\n")


def main():
    _retired()
    mp.set_start_method("spawn", force=True)
    print("Building catalog (timeout-verified)...", flush=True)
    specs, log_rows = build_all()
    total = 0
    for s in specs:
        total += write_unit(s, s["drills"])
    update_indexes(specs, log_rows)
    print(f"DONE units={len(specs)} drills_new={total}", flush=True)
    print("UNITS:", [s["uid"] for s in specs], flush=True)


if __name__ == "__main__":
    main()
