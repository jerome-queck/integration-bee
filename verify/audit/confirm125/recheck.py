"""r4: rerun ids not CONFIRMED in results.tsv; shard k of N; writes recheck_k.tsv (resumable)."""
import sys, os, signal
import confirm125 as c, json
k, N = int(sys.argv[1]), int(sys.argv[2])
rows = {json.loads(l)["id"]: json.loads(l) for l in open(c.REPO + "/problems/records.jsonl") if l.strip()}
bad = sorted({l.split("\t")[0] for l in open(c.OUT) if l.split("\t")[1] not in ("status", "CONFIRMED")})
mine = [i for j, i in enumerate(bad) if j % N == k]
out = os.path.join(os.path.dirname(c.OUT), f"recheck_{k}.tsv")
done = {l.split("\t")[0] for l in open(out)} if os.path.exists(out) else set()
for i in mine:
    if i in done: continue
    signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError("row timeout 1800s"))); signal.alarm(1800)
    try: o = c.run(i, rows)
    except Exception as ex:
        o = dict(id=i, status="ERROR", value="", answer="", rel_err="", tol="", params="", secs="", method=f"{type(ex).__name__}: {str(ex)[:200]}".replace("\t"," ").replace("\n"," "))
    signal.alarm(0)
    with open(out, "a") as f: f.write("\t".join(str(o[x]) for x in ("id","status","value","answer","rel_err","tol","params","secs","method")) + "\n")
    print(i, o["status"], flush=True)
print("DONE", flush=True)
