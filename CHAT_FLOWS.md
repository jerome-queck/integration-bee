# Chat flows (Jerome never runs the CLI)

The companion is the only human interface. It sends one JSON turn to `scripts/control-integration-bee turn apply`. The CLI writes learner state. That includes the projection `progress.local.json`. The companion does not edit that file.

`turn schema` prints the request and result shapes. `turn show` reads the session and does not write.

## Flow 1 — Teach a concept

Send `{"kind":"teach"}`. Read the path in `drill.teaching`. Say the integral in `drill.latex`. Do not show an answer. When the learner answers, send a mark turn.

## Flow 2 — Mark a photo

Read the photo, or take a typed final answer. For a photo, set `source` to `photo`, put the expression in `extract.final_answer`, and set `image` to the chat file path. The CLI copies that file to `submissions/<IB_USER>/` under the data directory and returns `mark.picture`. `progress show` lists the same relative path. `IB_USER` defaults to `default`. A second learner uses a separate `IB_DATA_DIR`. A typed answer sets `source` to `typed` and omits `image`. A manual problem also needs `verdict` set to `correct` or `incorrect`. Speak `say`. Do not invent a mark scheme. Do not commit the copied file.

## Flow 3 — Timed mock

Send `{"kind":"mock-start"}`. Send `"cold": true` only when the learner explicitly wants a cold mock. The result includes `duration_minutes` and `mock.started` in Asia/Singapore. Serve `problems` in words. Mark each answer with a photo or a typed final. Then send `mock-finish` with the score and the missed ids.

## Rules

- No CLI steps for the learner.
- An empty message sends `{"kind":"empty"}` and uses `say`.
- The CLI blocks a timed mock until every Round 1 node is solid.
- SAMPLE-Q17 is graded by the CLI. `ln|ln x|+C` matches. The answers PDF value `e^x+C` does not.
