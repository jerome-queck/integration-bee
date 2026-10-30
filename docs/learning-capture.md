# Learning capture

Any agent that teaches a concept or gives a solution updates the pack when the checkout is wrong or incomplete. The learner never edits the repo. A live study turn does not edit it either. Capture is a later pull request that uses the files and gates below. An external sticky handoff uses this same list.

GitHub tip is the source of truth. A fleet copy of `STATE.md` is not in this repo and does not authorize a write.

## Solution skepticism

Any agent that touches a solution has the right, and the duty, to question it, without slowing the work:

- Run `make sanity` (rows changed against `origin/main`) or `make sanity IDS="<id> ..."`. It differentiates indefinite answers and integrates definite ones numerically, in seconds.
- Do not hold the learner reply or the current pull request for it. Flag a `MISMATCH` in the reply or pull request and fix it in a follow-up pull request after checking the problem source.
- `UNCONFIRMED` means the numerics could not decide. Leave the row listed; never label a problem impossible.

## Two writers

| Writer | May change | May not change |
|---|---|---|
| `scripts/control-integration-bee turn apply` | Learner files under the data directory: `session.json`, `attempts.json`, `heatmap.json`, `mocks.json`, `journal.json`, `streaks.json`, `skill-ticks.json`, `marks.json`, `stickies.json`, the projection `progress.local.json`, and a photo copy in `submissions/<IB_USER>/`. | `problems/records.jsonl`, `solutions/`, `units/`, `pedagogy/`, `docs/techniques/`, `verify/`, `trackers/catalog.json`. |
| A repo agent, in a pull request | The pack files named for that process below. | `progress.local.json`, `trackers/live/`, `.venv/`, a plaintext Yang guide, `Resource_pack.zip`. Do not edit `AGENTS.md` by hand. |

`doctor` does not write. `problems list`, `problems select`, and `problems show` only read. `scripts/import_resource_catalog.py` rewrites `problems/records.jsonl` from an extract, keeps sample rows, and refuses a catalog the checker rejects. It is not the path for one derived answer.

The companion skill, `pedagogy/README.md`, `CHAT_FLOWS.md`, and `docs/decisions/0005-turn-contract.md` still govern the live turn. `verify/gap_index.py` requires the sentence "A study session does not edit a teaching note." That sentence forbids a pack edit inside the turn. It does not forbid the follow-up pull request in this file.

On an unchecked row the live turn says the source prints no answer, sends no `verdict`, and does not treat a chat derivation as a grade. `turn apply` then returns `unchecked catalog problem has no printed answer` and writes nothing.

## A — Teach a unit or concept

Trigger: a miss whose named note lacks the move, a new recognition exercise, or a coach card that no longer matches its unit.

Required update, in a later commit:

- The one file `say` named. That is `units/<unit>/teaching.tex` or the technique note in `docs/techniques/beyond-yang.md`.
- `units/<unit>/teaching.md` only when the pointer is wrong. The lesson is the `.tex` file.
- `units/<unit>/meta.yaml` when tags, Yang sections, or file names change.
- A coach card under `docs/techniques/concepts/`, plus the row in `pedagogy/concept-map.md`, when the inventory changes. Cards are not gap ids (`docs/decisions/0014-concept-cards.md`).
- An optional node's `drill_ids` and `teaching` fields in `trackers/catalog.json`, checked by `verify/teaching_catalog_check.py` (`docs/decisions/0017-ready-syllabus-lessons.md`).

The added example is original, or it cites a stored drill id. `verify/gap_index.py` rejects `R1-`, `R2-`, `R3-`, and `YANG-` inside a gap note, and it rejects an extra file placed directly in `docs/techniques/`. New cards go in `docs/techniques/concepts/`.

A new machine drill also updates `verify/drills_unitN.json`, `drills.md`, `drills.tex`, and `solutions.tex`. `teaching.tex`, `drills.tex`, and `solutions.tex` start by inputting `templates/technique-note.tex`, `templates/drill-sheet.tex`, and `templates/solution-sheet.tex` (`scripts/check_templates.py`). `doctor` prints `drills=` plus the combined length of those JSON files (300 at this tip). `.agents/skills/verify-integration-bee/features/doctor.md` and `verify.md` require `drills=300` and `PASS check_math (300 drills + spotchecks)`. Update those sentences in the same pull request. `AGENTS.md` recounts the files when regenerated.

Allowed writer: a repo agent, after the study turn. The turn itself only stores the attempt.

## B — Coach a contest or sample row that already has an official solution

Trigger: the learner has answered, and `problems show` has a cited answer. Every resource-pack id has `solutions/pack/<id>.md`. Every sample id has `solutions/sample/<id>.md`.

Required update: none, when the note, the cited PDF, and the catalog agree.

Read the note only after the learner answers. Grade from the catalog:

| `verify` | Live turn | CLI |
|---|---|---|
| `sympy` | Send `extract.final_answer`. Omit `verdict`. | Compare with `answer_sympy`. |
| `manual` | Send `verdict` `correct` or `incorrect` after reading `answer_plain` and the note. | Store that verdict. There are no resource-pack manual rows at this tip. A synthetic fixture still covers the verdict path. |
| `unchecked` | Say the source prints no answer. Omit `verdict`. | Write nothing. |

`has_worked` is true only when `worked_solution_origin` is `pdf_copy`. A markdown note does not set it. Do not treat `worked_solution_plain` as the coach's writeup; that field is an extract and can be the wrong problem (`docs/decisions/0016-pack-source-holds.md`).

Allowed writer: the CLI, for the attempt only.

## C — Solve an integral with no official worked solution

Trigger: you derive a final the cited PDF does not print, or the markdown note is absent.

Required update, in one pull request:

1. `solutions/pack/<id>.md`, `solutions/yang/<id>.md`, or `solutions/sample/<id>.md`.
2. Header lines that say the printed answer is absent and `Worked source: derived in this note`, or that name the PDF page when a final is printed and only the steps are new.
3. Sections `Problem`, `Solution`, `Final answer`, and `SymPy self-check` when SymPy closes the identity. Point at the certificate module the check actually runs.
4. Catalog fields only as the gate allows. See the field recipe below.

Origins are `missing`, `pdf_copy`, and `derived`. A Yang row stores a repo-written worked solution in `worked_solution_plain` and `worked_solution_latex` together, with `worked_solution_origin` `derived`; all 275 Yang rows do, `has_worked` is true for them, and the pdf_copy count does not include them. A `pdf_copy` row still stores an extract in `worked_solution_plain` and keeps `worked_solution_latex` null. Sample rows must keep `worked_solution_origin` `missing`, an empty `worked_solution_plain`, and a `notes` string that contains `solutions/sample/<id>.md`.

`solutions/README.md` still says these notes do not change `problems/records.jsonl` and still indexes an older manual-pack list. That page is a historical index. This file is the capture procedure. `solutions/self_check.py` re-proves the ids it lists and does not read the catalog.

Allowed writer: a repo agent. The study turn says the note is missing and does not create it (`pedagogy/README.md`).

## D — Yang practice rows that are unchecked

Trigger: a Yang row with `verify: unchecked`. After the §1.9 split, the §1.20 page-image proof, and the exclusion of formula `YANG-1.14-P10`, no Yang pack row remains unchecked. `YANG_WITH_ANSWER` lists the proved Yang ids: the §1.1 textbook list, the §1.2 list, `YANG-1.3-Ex01`, `YANG-1.3-Ex02`, `YANG-1.3-Ex03`, the §1.4 and §1.5 practice lists, the §1.6 and §1.7 lists, the Lane L4 §1.8 and §1.11 practice lists, the §2.3 list `YANG-2.3-P01`–`P18`, the §2.4 list `YANG-2.4-P01`–`P12`, the §2.5 and §2.6 rows the gate accepted, the Lane L8 rows in sections 2.7, 3.4, 3.8, 4.4, 4.6, 6.1, and 6.7, the Lane L5 rows in §§1.12, 1.15, 1.17, 1.18, and 1.20, the §1.9 examples `YANG-1.9-P01a`–`P01c` and `YANG-1.9-P04a`–`P04b`, and `YANG-1.20-P01`.

The live turn does not fill the row. A fill is its own pull request for one id, and only when you are changing the catalog on purpose:

- `problems/records.jsonl` for that id: `answer_plain` and `answer_source_pdf` together, or both empty. A `sympy` row also needs `answer_sympy`, `sympy_expr`, `integrand_latex`, `answer_latex`, `variable`, `kind`, and `limits`. `worked_solution_latex` stays null.
- `verify/problem_catalog.py`: add the id to `YANG_WITH_ANSWER`. Set `EXPECTED_SYMPY` or `EXPECTED_MANUAL` to the new totals. `catalog_problem` rejects any other answered Yang id, any sympy Yang id outside that set, and a count mismatch.
- `solutions/yang/<id>.md` with the printed guide page. Copy a final the guide prints. A derived final is recorded in `docs/decisions/0010-sympy-pack-rows.md` and `docs/decisions/0016-pack-source-holds.md`. Rows the gate does not prove stay unanswered.
- A proof `verify/pack_gate.py` accepts. Example 1 uses ordinary definite integration. Example 3 uses `verify/yang_certificates.py` for that integrand on `[0, 6]`. §1.4 item 3 uses the same module for `(2^x+3^x)/5^x` on `[0, ∞)`. `YANG-2.4-P12` uses it for `sec(x)^6 exp(-tan x)` on `[0, π/2]`. The same module certifies `YANG-2.6-P10`, `YANG-2.6-P12`, and `YANG-2.6-P14` when those printed integrands match. Other shapes return None. `scripts/recover_pack_math.py` does not gate Yang.
- `solutions/self_check.py` when that note's identity should be re-run there.

Do not edit a Yang row outside the batch you are proving. Do not set `answer_plain` alone. An unchecked row whose gate does not accept a final stays unchecked. `YANG-1.9-P01a`–`P01c` and `YANG-1.9-P04a`–`P04b` are the printed §1.9 examples, and `YANG-1.20-P01` is the page-image reading. `YANG-1.14-P10` is a reference formula excluded from the pack, not an integral.

`YANG-1.3-Ex02` is `verify: sympy`. The guide prints 2, and the even-part reduction in `verify/pack_gate.py` accepts that value. Its worked solution is now repo-written and checked, like `YANG-1.3-Ex03`, so `worked_solution_origin` is `derived`, not `pdf_copy`.

Allowed writer: a repo agent, in a pull request that moves the gate constants with the row. The companion is not that writer.

## E — Wrong mathematics found while teaching

Trigger: a stored final, a drill answer, a certificate, or a lesson disagrees with a checked derivation or with the cited PDF.

Required update, together, in one pull request:

- The worked note, preserving the conflicting printed mark.
- The catalog answer fields and the cite in `answer_source_pdf`.
- The certificate and the grading fixture that names the old value.
- `EXPECTED_SYMPY`, `EXPECTED_MANUAL`, and `EXPECTED_PDF_COPY` when a count changes.
- The unit drill files in process A when the bug is a concept drill.

Follow the escalation template in `docs/decisions/0016-pack-source-holds.md`. Certify the printed problem. Do not invent agreement with a wrong mark. Do not clear a source conflict by editing only the chat reply.

A lesson bug uses the file `say` named and an original example or an existing drill id. `verify/run.sh` must still fail a wrong drill answer.

Allowed writer: a repo agent. `scripts/recover_pack_math.py` is the writer of proved resource-pack SymPy fields (`docs/decisions/0010-sympy-pack-rows.md`). A hand edit of those fields has to match a proof the pack gate already accepts.

## F — Sticky handoff and a live teaching chat

Same pack list. A handoff does not keep a private ledger, and a live chat does not get a lighter one.

| Phrase in this repo | What it is | Writer |
|---|---|---|
| Learner sticky | One technique card in `stickies.json`, from `extract.method_note` on a correct mark. Strength is computed, not stored (`docs/decisions/0006-marks-and-stickies.md`). | `turn apply` only. |
| External sticky handoff | A repo task from outside the chat, including a handoff letter. | The same pull request as processes A–E. |

Learner stickies are not capture. Writing `stickies.json` by hand does not record a solution.

## G — What the CLI will not store

| Command or rule | Effect on capture |
|---|---|
| `doctor` | Reads the checkout. Creates no file. |
| `turn apply` | Writes learner state only. An unchecked mark writes nothing. |
| `turn schema`, `turn show` | Read. |
| `problems show` | Prints the stored cite. It does not accept a new answer. |
| `verify: sympy` | The companion's `verdict` cannot override a wrong expression. |
| `verify: manual` | Needs `verdict`. The CLI does not parse the lossy integrand. |
| `verify: unchecked` | No stored answer, so no grade. |
| `IB_DATA_DIR`, `IB_USER` | Separate learners. They do not select a pack branch. |
| `make check` | Re-proves stored expressions, catalog counts, templates, gap notes, and the turn fixtures. It does not open the PDFs. |

`progress tick`, `progress journal`, and `progress mistake` also write learner state only.

## Field recipe for a resource-pack `sympy` row

Set these together: `verify` `sympy`, `answer_plain`, `answer_source_pdf`, `answer_sympy`, `sympy_expr`, `integrand_latex`, `answer_latex`, `variable` (one of `x`, `t`, `X`, `e`, or `grid` for a grid), `kind`, `limits` (`[]` when the kind is not bounded, otherwise two strings). Leave `worked_solution_latex` null. Keep `worked_solution_plain` empty unless `worked_solution_origin` is `pdf_copy`, and then store an extract, not a new derivation. Yang rows are the exception (see the origins paragraph above): they store both texts with origin `derived`.

`verify/problem_catalog.py` holds `EXPECTED_COUNT` 948, `EXPECTED_SYMPY` 948, `EXPECTED_MANUAL` 0, and `EXPECTED_PDF_COPY` 193 for pack rows after the §1.9 split, the §1.20 page-image proof, and the exclusion of formula `YANG-1.14-P10`. Sample rows are 20 and all `sympy` at this tip; they are outside those totals. The reference row is outside those totals as well. Recount after rebasing. Do not copy a historical total out of `docs/decisions/0016-pack-source-holds.md`.

## Checks before the pull request

```bash
scripts/control-integration-bee doctor
make check
```

`doctor` prints `READY integration-bee`. `make check` is the catalog, certificate, turn, template, and formal gate. Open the pull request. Do not merge it here.
