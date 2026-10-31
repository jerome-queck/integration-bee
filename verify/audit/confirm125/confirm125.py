"""Resumable confirmation of the 125 rows left UNCONFIRMED by /workspace/audit-skep.
Usage: confirm125.py [ID ...]   (no args: all ids in ids.txt not yet in results.tsv)
Appends one TSV row per id: id, status, value, answer, rel_err, tol, method."""
import hashlib, os, sys, json, time, signal, traceback
REPO = os.environ.get("IBE_REPO", "/workspace/repos/ibe-confirm")
sys.path[:0] = [REPO + "/verify", REPO + "/scripts", os.path.dirname(__file__)]
import sympy as sp, mpmath as mp
import pack_gate, checks
OUT = os.path.join(os.path.dirname(__file__), "results.tsv")
OVERRIDE = {"R1-2020-Q16": {"k": "7/10"}, "R1-2020-Q25": {"a": "3", "b": "2"},
            "R2-2021-Group-Q06": {"a": "27/10", "b": "13/10"},
            "R2-2025-SG-Relay-Q03": {"m": "2", "n": "2"}, "R2-2025-UK-Relay-Q03": {"m": "2", "n": "2"}}
PARAMS = ["13/10", "27/10", "7/4"]; INTS = ["2", "3", "1"]
PINS = os.path.join(os.path.dirname(__file__), "expr_pins.json")

def expression_pin(row):
    payload = json.dumps({
        "sympy_expr": row.get("sympy_expr"),
        "limits": row.get("limits"),
        "variable": row.get("variable"),
        "kind": row.get("kind"),
    }, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()

def rejects_unbound_expression(ident, row) -> bool:
    """True when this row is not the expression the id's check was pinned to."""
    try:
        pins = json.load(open(PINS, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return True
    pinned = pins.get(ident)
    if not pinned:
        return True
    return expression_pin(row) != pinned

def param_point(r, x):
    exprs = [pack_gate._parse(r["sympy_expr"], r["variable"]), pack_gate._parse(r["answer_sympy"], r["variable"])]
    exprs += [pack_gate._parse(t, r["variable"]) for t in r.get("limits") or []]
    free = set().union(*[e.free_symbols for e in exprs]) - {x}
    free = {s for s in free if s.name not in ("k", "j", "shuttle_value", "rounded_value", "t", "y", "z") or r["id"] in OVERRIDE and s.name in OVERRIDE[r["id"]]}
    P = {}
    for i, s in enumerate(sorted(free, key=str)):
        P[s.name] = INTS[i % 3] if s.is_integer else PARAMS[i % 3]
    P.update(OVERRIDE.get(r["id"], {}))
    return P

def answer_value(r, x, P):
    F = pack_gate._parse(r["answer_sympy"], r["variable"])
    sub = {s: sp.Rational(P[s.name]) for s in F.free_symbols if s.name in P}
    F = F.subs(sub)
    if F in (sp.oo, -sp.oo): return mp.inf if F == sp.oo else -mp.inf
    return mp.mpf(sp.N(F, 60))

def run(i, rows):
    r = rows[i]
    if rejects_unbound_expression(i, r):
        return dict(id=i, status="MISMATCH", value="", answer="", rel_err="", tol="", params="", secs=0,
                    method="sympy_expr is not the pinned expression for this id")
    x = pack_gate.namespace(r["variable"])[r["variable"]]
    mp.mp.dps = 40
    P = param_point(r, x)
    t0 = time.time()
    checks.LAST_ERR[0] = None
    out = checks.C[i](P)
    val, method = out[0], out[1]
    opts = out[2] if len(out) > 2 else {}
    if "params" in opts: P.update(opts["params"])
    tol = opts.get("tol", mp.mpf(10)**-25)
    ans = answer_value(r, x, P)
    if mp.isinf(ans) or mp.isinf(val):
        ok = ans == val; err = 0 if ok else mp.inf
    else:
        err = abs(val - ans) / (1 + abs(ans)); ok = err <= tol
    if checks.LAST_ERR[0] is not None:
        method += f" [extrap_err~{mp.nstr(checks.LAST_ERR[0],2)}; |val-ans| within it: {bool(err <= 10*checks.LAST_ERR[0]+mp.mpf(10)**-30)}]"
    st = "CONFIRMED" if ok else "MISMATCH"
    return dict(id=i, status=st, value=mp.nstr(val, 30), answer=mp.nstr(ans, 30), rel_err=mp.nstr(err, 3),
                tol=mp.nstr(tol, 2), params=json.dumps(P), secs=round(time.time()-t0, 1), method=method)

def main():
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(REPO + "/problems/records.jsonl") if l.strip()}
    recheck = sys.argv[1:2] == ["--recheck"]
    if recheck: sys.argv = sys.argv[:1]
    ids = sys.argv[1:] or open(os.path.join(os.path.dirname(__file__), "ids.txt")).read().split()
    done = set()
    if os.path.exists(OUT):
        L = open(OUT).read().splitlines(True)
        if recheck:
            L = [l for l in L if l.split("\t")[1] in ("status", "CONFIRMED")]
            open(OUT, "w").writelines(L)
        done = {l.split("\t")[0] for l in L}
    else: open(OUT, "w").write("id\tstatus\tvalue\tanswer\trel_err\ttol\tparams\tsecs\tmethod\n")
    for i in ids:
        if i in done and len(sys.argv) == 1: continue
        try:
            signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError('row timeout 1800s')))
            signal.alarm(1800)
            o = run(i, rows)
            signal.alarm(0)
        except Exception as ex:
            signal.alarm(0)
            o = dict(id=i, status="ERROR", value="", answer="", rel_err="", tol="", params="", secs="",
                     method=f"{type(ex).__name__}: {str(ex)[:200]}".replace("\t", " ").replace("\n", " "))
        line = "\t".join(str(o[k]) for k in ("id", "status", "value", "answer", "rel_err", "tol", "params", "secs", "method"))
        with open(OUT, "a") as f: f.write(line + "\n"); f.flush(); os.fsync(f.fileno())
        print(i, o["status"], o["rel_err"], o["secs"], flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
