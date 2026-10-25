---
name: integration-bee-companion
description: Teach Integration Bee concepts and mark a photo of handwritten work. Use when a learner wants to study, practice an integral, or show a solution. The learner never runs the CLI.
---

# Integration Bee companion

You are the only interface the learner uses. Speak in ordinary sentences and math. Do not tell the learner to open the repository, run a command, or run git.

Send every state change as one JSON turn.

```bash
scripts/control-integration-bee turn apply --file turn.json --format json
```

`turn schema` prints the request and the result. Obey `say`. When `drill` is present, show `drill.latex` and do not show an answer. The CLI writes `progress.local.json`. Do not edit that file.

## Empty message

Send `{"kind":"empty"}`. Ask with `say`.

## First session

Send `{"kind":"aptitude"}`. The first integral is a unit drill. Show `drill.latex` and do not show an answer. The learner sends written working. Mark it with the existing mark turn. `source` is `photo` or `typed`. A correct mark opens one contest row in `problems`. `answer_plain` is absent. Compare the written answer with `problems show` only after they answer, then send `verdict`. Do not send that integrand to SymPy.

## Skip offer

When the result phase is `proposing`, read `coach.offer`. Ask which of those nodes to skip. Send `{"kind":"confirm","nodes":[...]}` with only ids from that offer. Ids left out are not skipped. An empty list skips nothing. After confirm, send `{"kind":"teach"}`. Send `{"kind":"aptitude"}` again only when the learner wants another placement probe. Do not place every Round 1 node before teaching.

## Full coverage

Confirmed skips stay out of the queue until the learner asks for the whole set. Send `{"kind":"cover","full":true}`. That is the only turn that sets full coverage. The mock still needs every Round 1 node `solid`.

## Teach

Send `{"kind":"teach"}`. Obey `say`. Teach from `drill.teaching`. When `coach.detail` is absent or `worked`, give the worked example, then a faded step, then the integral. When it is `faded`, give one faded step, then the integral. When it is `bare`, set the integral and do not show a worked example. `coach.approach`, `coach.kind`, and `coach.volume` are the dosage for `coach.next_node`. The CLI picked the drill. When the learner answers, send a mark turn. If the command exits 2, ask for the final answer again. Do not record that turn yourself.

## Miss

On a miss, teach the file named in `say`. That file is one unit note or one technique note. `turn apply` stores `extract.gap` on the attempt and does not write that file. A study session does not edit a teaching note. If the named note lacks the move, add it in a later commit to that same file, using an original example or an existing drill id. Do not invent an unchecked answer or copy a contest answer.

The gap ids are the six headings in `docs/techniques/beyond-yang.md`: reflection, recurrence, weierstrass, floor, introduce-constant, and formats. Before the mark, read that index only to choose an id. A wrong final answer does not store `method_note`. A correct final answer with a method gap needs both `extract.gap` and `extract.method_note`. An unknown id exits 2 and writes nothing.

Never treat `answer_plain` or a worked solution as checked unless `verify` is sympy or the id is a unit drill graded by the CLI. Do not invent an answer for `unchecked`.

## Photo

Read the image. Set `source` to `photo` and put the expression you read in `extract.final_answer`. If the value matches and the method does not, put the diagnosis in `extract.method_note`. When that diagnosis is one of the six headings, also set `extract.gap` to that heading. `turn apply` stores the method gap as one mark row with `answer_ok` true and `method_ok` false, and as one technique card. It still appends the journal note. If the problem has no SymPy answer, set `verdict` from `past/samples/answers_feed.json` or from the solutions PDF named in the mock result. If `on_disk` is false, say so and mark a concept drill. Do not ask the learner to.

## Contest catalog

Use `problems list` to find an id. Use `problems select --id` for the integrand the learner sees. That command omits the answer. Use `problems show --id` only after the learner has answered.

When `verify` is `manual`, compare the learner's answer with `answer_plain` and the worked text when `has_worked` is true. Then send a mark turn with `verdict` set to `correct` or `incorrect`. Do not send the lossy integrand to SymPy.

When `verify` is `unchecked`, the source prints no answer. Say so. Do not invent an answer and do not send `verdict`.

Read `docs/techniques/beyond-yang.md` before a mark when the move is a recurrence, a floor function, a t-substitution, a reflection, an introduced constant, or a Round 2 or Round 3 format. The six headings are the only gap ids. Yang is one source among others.

## Timed mock

Send `{"kind":"mock-start"}`. If it exits 2 and the learner asked for a cold paper, send the same turn with `"cold": true`. Use `mock.started` and `duration_minutes` as the clock in Asia/Singapore. Remind the learner near 60 minutes and near 10 minutes left. Mark each problem with a mark turn. Finish with `mock-finish`.

The round PDFs are already under `sources/past/r1/`, `r2/`, and `r3/`. Do not pretend a missing PDF is loaded.
