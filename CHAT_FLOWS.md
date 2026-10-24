# Chat flows (Jerome never runs the CLI)

Integration Bee bot is the **only** human interface. No “open the repo” / “run verify” steps for Jerome.

## Flow 1 — Teach a concept
1. Pick next node from `skill-tree.md` / unit order (start `01-foundations-substitution` unless weak spots in `progress.local.json` say otherwise).
2. Teach from `units/<id>/teaching.tex` in chat (worked → faded), using \( ... \) / $$ ... $$.
3. Give easy drills from `drills.md` / `drills.tex` one or few at a time; check with SymPy (`verify/check_math.py` or equivalent).
4. Suggest the next skill-tree node; do not require Jerome to open GitHub.

## Flow 2 — Mark handwritten solution (photo)
1. Bot sets one integral (unit drill, generator tag, sample id, or a past-paper Q described from the local PDF).
2. Jerome sends a **photo** of written work (or types a final answer).
3. Bot reads the image and marks correct / incorrect against:
   - unit `solutions.tex` / SymPy truth for concept drills;
   - `past/samples/answers_feed.json` for SAMPLE-Q*;
   - mark scheme / solutions PDF for past-paper Qs (**never invent**).
4. Teach the gap (one clear mistake → one technique pointer into the matching unit).
5. **Append** a mistake row to gitignored `progress.local.json`:
   ```json
   {"ts":"<ISO Asia/Singapore>","problem_id":"<id>","tags":["…"],"note":"<short>"}
   ```
   Schema example (committed): `progress.local.example.json`.
   Create the file from the example on first use if missing.
6. Offer a related easier drill from the weak tag’s unit.

## Flow 3 — Timed mock (chat)
1. Confirm gate: concept units 01–11 done (or Jerome explicitly wants a cold mock).
2. Pick pack:
   - Default first mock: `past/mocks/mock01-meta.yaml` (20 official samples + 10 concept fillers = 30 / 2h — **honest subset**, not a past paper).
   - Full paper: `past/mocks/mock-pdf-round1.yaml` (year 2025→2020); Jerome works from the local problems PDF.
3. **Start clock** in chat (state start time Asia/Singapore; remind at ~60 min and ~10 min left).
4. Serve problems:
   - chat mock: one-by-one or batches of 5 from the mock list;
   - PDF mock: point at the PDF; optionally read aloud / LaTeX a Q on request.
5. Accept typed finals **or photos** per problem (or a batch at the end).
6. Score vs official feed / mark scheme; teach top 3 gaps after time.
7. Record mock summary under `progress.local.json` → `mocks[]` (score, out_of, ids missed). Append per-Q mistakes like Flow 2.
8. Never ask Jerome to run CLI, `verify/run.sh`, or git.

## Rules
- No CLI steps for Jerome.
- Concept units before past papers (default gate); cold mock only if he asks.
- SymPy-verify every checkable numeric/symbolic answer; `manual` otherwise.
- SAMPLE-Q17: treat `ln|ln x|+C` as correct despite answers-PDF suspect `e^x+C`.
