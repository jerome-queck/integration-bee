#!/usr/bin/env python3
"""Fail when a row's answer_plain drifts from its canonical answer_sympy.

answer_plain is the human display of the answer. It may use unicode (pi, sqrt,
superscripts), ln/arctan/cot^-1 spellings, implicit multiplication, and a
trailing "+ C" on an antiderivative. After normalising those, it must parse
with SymPy and equal answer_sympy: exactly at sample points for definite and
other rows, and up to an additive constant (derivative check) for indefinite
rows. Rows with no answer_plain (unchecked) are skipped, and grid rows are left
to verify/pack_grid.py, which checks their printed clue map.

  python3 verify/answer_plain_check.py            # check problems/records.jsonl
  python3 verify/answer_plain_check.py --self-test
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, standard_transformations)

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"
TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
WORDS = [("π", " pi "), ("−", "-"), ("–", "-"), ("·", "*"), ("×", "*"), ("∞", "oo"),
         ("γ", " EulerGamma "), ("ζ", "zeta"), ("Γ", "gamma")]
FUNCS = [(r"\b(sin|cos|tan|cot|sec|csc|sinh|cosh|tanh)\s*(?:−|-)\s*1\b", r"a\1"),
         (r"\barc(sin|cos|tan|cot|sec|csc)\b", r"a\1"), (r"\bln\b", "log")]
# A display written in a parameter the symbolic fields re-encode; each is cited in the row notes.
DISPLAY_BINDINGS = {"SAMPLE-Q08": {"s": "1 + sigma + I*tau"}}  # notes: "s=1+sigma+i*tau"
# Mixed signs. All-positive samples make Abs(a) and a agree, so a display
# without the absolute value matches a canonical answer that has one.
POINTS = (sp.Rational(13, 10), sp.Rational(-27, 10), sp.Rational(7, 4))
INT_POINTS = (2, 3, 1)


def normalise(text: str) -> str:
    s = text.strip()
    s = re.sub(r"([^\s(])([²³⁴⁵⁶⁷⁸⁹⁰¹]+)", lambda m: f"{m.group(1)}**({m.group(2).translate(SUP)})", s)
    for a, b in WORDS:
        s = s.replace(a, b)
    for pat, rep in FUNCS:
        s = re.sub(pat, rep, s)
    s = re.sub(r"√\s*\(", "sqrt(", s)
    s = re.sub(r"√\s*([A-Za-z0-9_.]+)", r"sqrt(\1)", s)
    s = re.sub(r"\|([^|]+)\|", r" Abs(\1)", s)
    s = re.sub(r"\s*\+\s*C\s*$", "", s)
    return _power_calls(s)


def _power_calls(s: str) -> str:
    """Rewrite f^n(arg) as f(arg)**n, the usual sec^2(u) spelling."""
    while (m := re.search(r"\b([a-z]+)\s*\^\s*(\d+)\s*\(", s)):
        depth, i = 0, m.end() - 1
        for i in range(m.end() - 1, len(s)):
            depth += {"(": 1, ")": -1}.get(s[i], 0)
            if depth == 0:
                break
        s = f"{s[:m.start()]}{m.group(1)}{s[m.end() - 1:i + 1]}**{m.group(2)}{s[i + 1:]}"
    return s


def parse_plain(text: str, symbols: dict):
    local = {"cbrt": lambda a: sp.real_root(a, 3), "elliptic_F": sp.elliptic_f,
             "e": sp.E, "E": sp.E, "G": sp.Catalan, "pi": sp.pi, "I": sp.I, **symbols}
    return parse_expr(normalise(text), local_dict=local, transformations=TRANSFORMS)


def _values(expr, syms):
    """One distinct sample per symbol, plus a point outside the fixed triple.

    Giving every symbol the same value makes a+b match 2*a. A cubic that
    vanishes on POINTS matches x at those three samples and nowhere else.
    """
    ordered = list(syms)
    pts = []
    span = len(POINTS)
    for j in range(span):
        binding = {}
        for i, symbol in enumerate(ordered):
            k = (j + i) % span
            binding[symbol] = INT_POINTS[k] if symbol.is_integer else POINTS[k]
        pts.append(binding)
    extra = {}
    for i, symbol in enumerate(ordered):
        extra[symbol] = (5 + i) if symbol.is_integer else (sp.Rational(11, 3) + i)
    pts.append(extra)
    return pts


def _zero(expr) -> bool:
    v = sp.N(expr, 30)
    try:
        return abs(complex(v)) < 1e-20
    except TypeError:
        return False


def equivalent(plain, canon, kind: str) -> bool:
    if not isinstance(canon, sp.Expr) or not isinstance(plain, sp.Expr):
        return sp.srepr(plain) == sp.srepr(canon) or bool(sp.simplify(sp.Eq(plain, canon)) is sp.true)
    # Sample points are real, so give plain symbols real assumptions (d|x|/dx needs them).
    real = {v: sp.Symbol(v.name, real=True) for v in canon.free_symbols | plain.free_symbols
            if v.is_real is None}
    diff = (plain - canon).subs(real)
    syms = sorted(diff.free_symbols, key=str)
    if kind.endswith("indefinite") and not syms:
        return True  # antiderivatives agree up to a constant
    if kind.endswith("indefinite"):
        x = next((s for s in syms if s.name == "x"), syms[0])
        diff = sp.diff(diff, x)
        syms = sorted(diff.free_symbols, key=str)
    if syms and getattr(diff, "is_polynomial", lambda *_: False)(*syms) and sp.expand(diff) != 0:
        return False
    pts = _values(diff, syms) if syms else [{}]
    usable = 0
    for point in pts:
        try:
            if not _zero(diff.subs(point)):
                return False
            usable += 1
        except Exception:
            continue
    return usable > 0


def _display_equality(plain: str) -> list[str] | None:
    """Two sides of one top-level display '=', ignoring >=, <=, ==, and !=."""
    depth = 0
    found = None
    for i, ch in enumerate(plain):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == "=" and depth == 0:
            prev = plain[i - 1] if i else ""
            nxt = plain[i + 1] if i + 1 < len(plain) else ""
            if prev in "<>!" or nxt == "=":
                continue
            if found is not None:
                return None
            found = i
    if found is None:
        return None
    return [plain[:found].strip(), plain[found + 1 :].strip()]


def check_row(row: dict) -> str | None:
    plain = str(row.get("answer_plain") or "")
    if row.get("kind") == "grid":
        return None  # grid displays are the printed clue map, checked by verify/pack_grid.py
    if not plain.strip():
        if str(row.get("answer_sympy") or "").strip():
            return "answer_plain is blank"
        return None
    if row.get("kind") == "comparison":
        claim = "".join(plain.split())
        canon_text = str(row.get("answer_sympy") or "")
        name = canon_text
        try:
            parsed = sp.sympify(canon_text)
            if isinstance(parsed, sp.Symbol):
                name = parsed.name
        except Exception:
            name = canon_text
        if claim == "".join(str(name).split()):
            return None
        return f"answer_plain {plain!r} != answer_sympy {canon_text}"
    if plain.strip() == str(row["answer_sympy"]).strip():
        return None
    canon = sp.sympify(row["answer_sympy"])
    symbols = {s.name: s for s in getattr(canon, "free_symbols", set())}
    for name, value in DISPLAY_BINDINGS.get(row.get("id"), {}).items():
        symbols[name] = sp.sympify(value, locals=symbols)
    # A display equality passes when a parsed side matches and no parsed value disagrees.
    # "1=2" disagrees. A bare name such as φ, or a side the printer could not parse, does not.
    sides = _display_equality(plain) or [plain]
    if _display_equality(plain) is not None and any(not side for side in sides):
        return f"answer_plain has an empty side: {plain!r}"
    errors = []
    matched = 0
    for side in sides:
        try:
            got = parse_plain(side, symbols)
        except Exception as ex:  # noqa: BLE001 - any parse failure is drift
            errors.append(f"answer_plain does not parse ({type(ex).__name__}): {plain!r}")
            continue
        try:
            agrees = equivalent(got, canon, str(row.get("kind") or ""))
        except Exception as ex:  # noqa: BLE001
            errors.append(f"cannot compare ({type(ex).__name__}): {plain!r} vs {row['answer_sympy']}")
            continue
        if agrees:
            matched += 1
            continue
        if isinstance(got, sp.Symbol):
            continue
        errors.append(f"answer_plain {plain!r} != answer_sympy {row['answer_sympy']}")
    if matched and not any("!=" in item or "cannot compare" in item for item in errors):
        return None
    return errors[-1] if errors else f"answer_plain {plain!r} != answer_sympy {row['answer_sympy']}"


def self_test() -> None:
    good = [("π²/4", "pi**2/4", "definite"), ("π ln 2", "pi*log(2)", "definite"),
            ("2 arctan(3)", "2*atan(3)", "definite"), ("tan−1(x) + C", "atan(x) + 5", "indefinite"),
            ("(1/e) ln(√2 + 1)", "exp(-1)*log(1 + sqrt(2))", "definite"), ("1 −γ", "1 - EulerGamma", "definite"),
            ("ln|tan(x)| + C", "log(Abs(tan(x)))", "indefinite"), ("sec^2(x)", "sec(x)**2", "definite"),
            ("Γ(n) = (n−1)!", "gamma(n)", "definite")]
    vanish = f"(x-({POINTS[0]}))*(x-({POINTS[1]}))*(x-({POINTS[2]}))"
    bad = [("1", "1/4", "definite"), ("π\n4", "2 - pi**2/6", "definite"), ("2025", "2025*sin(1)**2/2", "definite"),
           ("tan(x)", "atan(x)", "indefinite"), ("   ", "1", "definite"), ("1=2", "1", "definite"),
           ("a + b", "2*a", "definite"), (f"x + {vanish}", "x", "definite")]
    for p, c, k in good:
        if check_row({"answer_plain": p, "answer_sympy": c, "kind": k}):
            sys.exit(f"FAIL self-test rejected {p!r} == {c}")
    for p, c, k in bad:
        if not check_row({"answer_plain": p, "answer_sympy": c, "kind": k}):
            sys.exit(f"FAIL self-test accepted {p!r} == {c}")


def main(argv: list[str]) -> int:
    self_test()
    if argv[1:2] == ["--self-test"]:
        print("PASS answer_plain self-test")
        return 0
    rows = [json.loads(l) for l in RECORDS.read_text().splitlines() if l.strip()]
    bad = [(r["id"], m) for r in rows if (m := check_row(r))]
    for i, m in bad:
        print(f"FAIL {i}: {m}")
    if bad:
        print(f"FAIL answer_plain drift: {len(bad)} of {len(rows)} rows")
        return 1
    print(f"PASS answer_plain matches answer_sympy for all {sum(1 for r in rows if r.get('answer_plain'))} rows with a display")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
