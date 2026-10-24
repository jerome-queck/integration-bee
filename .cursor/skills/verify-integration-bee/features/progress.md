# Progress

Progress stores a skill-tree tick and reads it back.

## Sub-features

- `progress-tick` sets `basic-integration` to `learning`.
- `progress-show` returns that tick.
- `progress-mock-blocked` refuses a mock before Round 1 nodes are solid.

## How to get to it (user POV)

- The companion marks a concept in progress after the learner has practiced it, and does not start a timed mock early.

## Driving it with control-integration-bee

Preconditions:

- `IB_DATA_DIR` has no `basic-integration` tick yet.

- **Tick.** Run `scripts/control-integration-bee progress tick --node basic-integration --status learning --format json | tee "$IB_EVIDENCE/tick.json"`. Exit code is 0.
- **Show.** Run `scripts/control-integration-bee progress show --format json | tee "$IB_EVIDENCE/show-after-tick.json"`. Stdout contains `basic-integration` and `learning`.
- **Blocked mock.** Run `scripts/control-integration-bee progress mock-start --format json >"$IB_EVIDENCE/mock.txt" 2>"$IB_EVIDENCE/mock.err"`. Exit code is 2. Stderr contains `round1 nodes not solid`.

## Gotchas

- `mock-start --cold` bypasses the Round 1 gate. The blocked proof must omit `--cold`.
- An unknown node exits 1 and must not be written.
