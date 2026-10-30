import confirm125 as c, json, sys
rows={json.loads(l)['id']:json.loads(l) for l in open(c.REPO+'/problems/records.jsonl') if l.strip()}
for i in sys.argv[1:]:
  try: o=c.run(i,rows); print(i,o['status'],o['rel_err'],o['value'],o['answer'],o['secs'],flush=True)
  except Exception as e: print(i,'ERR',repr(e)[:300],flush=True)
