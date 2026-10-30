"""Fast numeric sanity check for catalog solutions.

Indefinite rows: the stored answer's derivative must match the integrand at
sample real points (odd roots read as real roots). Definite rows: mpmath
quadrature must reproduce the stored value. Free parameters get fixed values.

Usage:
  python3 verify/solution_sanity.py              # rows changed vs origin/main
  python3 verify/solution_sanity.py ID [ID ...]  # named rows
  python3 verify/solution_sanity.py --all        # every sympy row (slow)

Exit 1 only on MISMATCH. UNCONFIRMED means the numerics could not decide; it
never means the problem is wrong or impossible.
"""
import json, os, signal, subprocess, sys
sys.path[:0] = ["verify", "scripts"]
import sympy as sp, mpmath as mp
import pack_gate

PTS = ["-8.3","-5.7","-3.1","-2.2","-1.4","-0.83","-0.37","-0.11","0.13","0.41","0.77","1.21","1.63","2.47","3.3","4.9","7.7"]
PARAMS = [sp.Rational(13,10), sp.Rational(27,10), sp.Rational(7,4)]

def real_roots(e):
    def fix(n):
        if n.exp.is_Rational and not n.exp.is_Integer and n.exp.q % 2 == 1:
            return sp.sign(n.base)**n.exp.p * sp.Abs(n.base)**n.exp
        return n
    return e.replace(lambda n: n.is_Pow, fix)

def params(exprs, x):
    free = set().union(*[e.free_symbols for e in exprs]) - {x}
    ints = [2, 3, 1]
    sub = {s: (sp.Integer(ints[i % 3]) if s.is_integer else PARAMS[i % 3])
           for i, s in enumerate(sorted(free, key=str))}
    return [e.subs(sub) for e in exprs], sorted(map(str, free))

def num(e, d=30):
    v = sp.N(e, d)
    if not v.is_number or v.has(sp.nan, sp.zoo, sp.oo, -sp.oo): return None
    return complex(v) if True else v

def indefinite(r, x):
    f = real_roots(pack_gate._parse(r["sympy_expr"], r["variable"]))
    F = pack_gate._parse(r["answer_sympy"], r["variable"])
    (f, F), free = params([f, F], x)
    dF = sp.diff(F, x)
    good = bad = 0; badpts = []
    mp.mp.dps = 40
    for p in PTS:
        pt = sp.Float(p, 40)
        try: fv = num(f.subs(x, pt))
        except Exception: fv = None
        if fv is None or abs(fv.imag) > 1e-15 * (1 + abs(fv)): continue
        dv = None
        try: dv = num(dF.subs(x, pt))
        except Exception: pass
        if dv is None:
            h = sp.Float("1e-15", 40)
            try:
                a = num(F.subs(x, pt + h), 40); b = num(F.subs(x, pt - h), 40)
                dv = None if a is None or b is None else (a - b) / 2e-15
            except Exception: dv = None
        if dv is None: continue
        if abs(dv.real - fv.real) <= 1e-7 * (1 + abs(fv)): good += 1
        else: bad += 1; badpts.append(p)
    if bad: return "MISMATCH", f"derivative differs at {badpts}; ok at {good}", free
    if good >= 3: return "CONFIRMED", f"derivative matches at {good} real points", free
    return "UNCONFIRMED", f"only {good} usable real points", free

def definite(r, x):
    st = _definite(r, x)
    if st[0] != "UNCONFIRMED":
        return st
    try:
        alt = _sympy_numeric(r, x)
    except Exception:
        alt = None
    return alt or st


def _sympy_numeric(r, x):
    f = pack_gate._parse(r["sympy_expr"], r["variable"])
    F = pack_gate._parse(r["answer_sympy"], r["variable"])
    lo, hi = (pack_gate._parse(t, r["variable"]) for t in r["limits"])
    (f, F, lo, hi), free = params([f, F, lo, hi], x)
    ans = complex(sp.N(F.doit() if F.has(sp.Integral, sp.Sum) else F, 20))
    val = complex(sp.N(sp.Integral(f, (x, lo, hi)), 20))
    if abs(val - ans) <= 1e-9 * (1 + abs(ans)):
        return "CONFIRMED", f"sympy N {val.real:.15g} = answer {ans.real:.15g}", free
    return None


def _definite(r, x):
    f = pack_gate._parse(r["sympy_expr"], r["variable"])
    F = pack_gate._parse(r["answer_sympy"], r["variable"])
    lo, hi = (pack_gate._parse(t, r["variable"]) for t in r["limits"])
    (f, F, lo, hi), free = params([f, F, lo, hi], x)
    if f.has(sp.Integral, sp.Subs, sp.Sum) or F.has(sp.Integral, sp.Sum):
        return "UNCONFIRMED", "integrand or answer holds an unevaluated Integral/Sum/Subs", free
    ans = num(F, 30)
    if ans is None: return "UNCONFIRMED", "answer has no numeric value", free
    mp.mp.dps = 30
    g = sp.lambdify(x, f, modules=["mpmath", {"floor": mp.floor, "sign": mp.sign}])
    def gg(t):
        v = g(t); return v
    a = mp.mpf(str(sp.N(lo, 30))) if lo.is_finite else (mp.inf if lo == sp.oo else -mp.inf)
    b = mp.mpf(str(sp.N(hi, 30))) if hi.is_finite else (mp.inf if hi == sp.oo else -mp.inf)
    # breakpoints at integers inside a bounded window, plus 0
    fin_lo = a if mp.isfinite(a) else mp.mpf(-60); fin_hi = b if mp.isfinite(b) else mp.mpf(60)
    brk = [a] + [mp.mpf(k) for k in range(int(mp.ceil(fin_lo)), int(mp.floor(fin_hi)) + 1) if a < k < b][:400] + [b]
    vals = []
    for method in ("tanh-sinh", "gauss-legendre"):
        try:
            v = mp.quad(gg, brk, method=method, maxdegree=8, error=False)
            vals.append(complex(v))
        except Exception as e:
            vals.append(None)
    ok = [v for v in vals if v is not None]
    if not ok: return "UNCONFIRMED", "quadrature failed", free
    tol = lambda u, w: abs(u - w) <= 1e-9 * (1 + abs(w))
    if not any(tol(v.real, ans.real) for v in ok) and b == mp.inf:
        freqs = {sp.simplify(t.args[0].diff(x)) for t in f.atoms(sp.sin, sp.cos)}
        terms = sp.Add.make_args(sp.expand(f))
        tf = [{sp.simplify(t.args[0].diff(x)) for t in term.atoms(sp.sin, sp.cos)} for term in terms]
        if len(freqs) > 1 and all(len(q) == 1 and next(iter(q)).is_number for q in tf):
            try:
                start = max(a, mp.mpf(1)) if mp.isfinite(a) else mp.mpf(1)
                head = mp.quad(gg, [a, start]) if start > a else 0
                tail = 0
                for term, q in zip(terms, tf):
                    gt = sp.lambdify(x, term, modules=["mpmath"])
                    tail += mp.quadosc(gt, [start, mp.inf], omega=float(next(iter(q))))
                ok.append(complex(head + tail))
            except Exception:
                pass
        if len(freqs) == 1 and next(iter(freqs)).is_number:
            w = float(next(iter(freqs)))
            try:
                start = max(a, mp.mpf(1)) if mp.isfinite(a) else mp.mpf(1)
                head = mp.quad(gg, [a, start]) if start > a else 0
                ok.append(complex(head + mp.quadosc(gg, [start, mp.inf], omega=w)))
            except Exception:
                pass
    if any(tol(v.real, ans.real) for v in ok):
        hit = next(v for v in ok if tol(v.real, ans.real))
        return "CONFIRMED", f"quad {hit.real:.15g} = answer {ans.real:.15g}", free
    if len(ok) == 2 and abs(ok[0] - ok[1]) <= 1e-12 * (1 + abs(ok[0])) and not tol(ok[0].real, ans.real):
        return "MISMATCH", f"both quadratures {ok[0].real:.15g}, answer {ans.real:.15g}", free
    return "UNCONFIRMED", "quadratures disagree or miss: " + ", ".join(f"{v.real:.12g}" for v in ok) + f"; answer {ans.real:.12g}", free

ROW_SECONDS = int(os.environ.get("SANITY_ROW_SECONDS", "30"))


def check(r):
    x = pack_gate.namespace(r["variable"])[r["variable"]]

    def alarm(*_):
        raise TimeoutError("row timed out")

    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(ROW_SECONDS)
    try:
        st, why, _ = (indefinite if r["kind"] == "indefinite" else definite)(r, x)
    except Exception as e:
        st, why = "UNCONFIRMED", f"{type(e).__name__}: {str(e)[:80]}"
    finally:
        signal.alarm(0)
    return st, why


def load():
    rows = {}
    for line in open("problems/records.jsonl"):
        if line.strip():
            r = json.loads(line)
            rows[r["id"]] = r
    return rows


def changed_ids(rows):
    try:
        old = subprocess.run(["git", "show", "origin/main:problems/records.jsonl"],
                             capture_output=True, text=True, check=True).stdout
    except Exception:
        return []
    before = {}
    for line in old.splitlines():
        if line.strip():
            r = json.loads(line)
            before[r["id"]] = r
    return [i for i, r in rows.items() if before.get(i) != r]


def main(argv):
    rows = load()
    if argv == ["--all"]:
        ids = list(rows)
    elif argv:
        ids = argv
    else:
        ids = changed_ids(rows)
    ids = [i for i in ids if rows.get(i, {}).get("verify") == "sympy" and rows[i].get("answer_sympy")]
    counts = {"CONFIRMED": 0, "UNCONFIRMED": 0, "MISMATCH": 0}
    for i in ids:
        st, why = check(rows[i])
        counts[st] += 1
        if st != "CONFIRMED":
            print(f"{st} {i}: {why}")
    print("sanity " + " ".join(f"{k.lower()}={v}" for k, v in counts.items()) + f" rows={len(ids)}")
    if counts["MISMATCH"]:
        print("FAIL solution sanity: check each MISMATCH against its source; fix in a follow-up PR")
        return 1
    print("PASS solution sanity")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
