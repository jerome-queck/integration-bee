# Repo Init Standard (DRAFT v0, 2026-10-13, not yet approved)

Every repo Code touches should have these before agents do feature work. Based on Lauren Tan's (poteto) pstack.
Her stance: "installing pstack alone does not get a team to her level; the verification skills and lint rules have to exist first" (Matt Pocock interview, 2 Oct 2026, as reported by https://developer.tenten.co/pstack-verification-agent-merge). Order of build: verification first, then context, then evidence, and only then parallel agents (The Neuron, Lesson #5: https://www.theneuron.ai/explainer-articles/pstack-explained-lauren-tans-system-for-trustworthy-ai-agents/).

Hard rules stay: changes land only through PRs. Code never merges or force-pushes without Jerome's OK. No bot starts work Jerome didn't ask for. Adding this standard to a repo is itself a PR, done only when Jerome names the repo.

## Checklist

| # | Item | Path | Proven by |
|---|---|---|---|
| 1 | AGENTS.md | `/AGENTS.md` | fresh agent sets up + runs `make check` from AGENTS.md alone |
| 2 | One-command check | `make check` (or `npm run check`) | same command green locally and in CI |
| 3 | Driver CLI | `scripts/control-<app>` (or `bin/`) | `control-<app> doctor` exits 0 on a fresh launch |
| 4 | verify-<app> skill | `.cursor/skills/verify-<app>/SKILL.md` | one full launch → doctor → drive → evidence → cleanup run, evidence survives |
| 5 | Feature map | `.cursor/skills/verify-<app>/features/` | every feature file driven live once; index matches files |
| 6 | Structure/type/lint rules | lint config + `scripts/check-*` | each custom rule fails on a real (or seeded) bad example |
| 7 | CI gates + branch protection | `.github/workflows/check.yml`, GitHub settings | PR with a deliberately broken test is blocked |
| 8 | Rule → enforcer table | section in AGENTS.md | every row names a file/check that exists |
| 9 | Decision & learnings log | `docs/decisions/` + `.audit/*.tsv` (uncommitted by default) | rows' evidence pointers resolve |
| 10 | PR template with evidence | `.github/pull_request_template.md` | template fields filled on the init PR itself |
| 11 | Isolation for parallel agents | documented ports/data dirs/env | two instances run side by side, or AGENTS.md says they can't |
| 12 | Check while you build (CHARTER 33) | `make check` + verify skill run during authoring; `docs/root-cause/` | builder's pre-PR run of the reviewer's checks is in the PR evidence; every issue caught twice has a check that fails on the real miss; 3+ review rounds have a root-cause note |

---

## 1. AGENTS.md
**What:** the first file any agent reads: what the app is, setup, the one check command, where the verify skill is, boundaries, approval gates, rule table.
**Why:** agents "see only the files [they] opened, copy the nearest example, and take the shortest path that compiles" (pstack `correct`). AGENTS.md is the entry point, but text is guidance only; anything costly to skip must be enforced elsewhere (pstack `correct` step 4: "Nothing fails when an agent skips them").
**Template:**
```md
# <app>
One paragraph: what it does, for whom.
## Setup
<exact commands from clean clone>
## Check (run before every PR)
make check   # lint + types + structure + tests
## Verify like a user
Use .cursor/skills/verify-<app>/ (feature map in features/).
## Boundaries
- Changes only via PRs. Never merge/force-push without Jerome's OK.
- Don't edit: <generated dirs, vendored code>
- Secrets: never read/print <paths>
## Rule → enforcer
| Rule | Enforced by |
|---|---|
| no direct DB access outside src/db | lint rule no-restricted-imports |
```
**Proof:** a fresh subagent given only the clone and "follow AGENTS.md" gets to a green `make check`. Any step it needed to guess becomes a fix.

## 2. One-command check
**What:** a single command for lint, types, structure checks, and tests.
**Why:** `correct`: "Run the same command locally and in CI." It gives agents one gate they can't misremember.
**Template:** `check: lint typecheck structure test` in Makefile / package.json.
**Proof:** CI job runs exactly this command; a deliberately failing test makes both fail.

## 3. Driver CLI (`control-<app>`)
**What:** a small CLI that launches the app, runs `doctor`, and drives it like a user (browser via CDP/Playwright, PTY/tmux for CLI/TUI, HTTP for services), and captures screenshots, ARIA snapshots, traces, and logs.
**Why:** Lauren's first skill at Cursor was "control glass": "the control or verification skill really has two components... the first part is obviously a CLI. So you want your agent to be able to reproducibly run the application and collect traces and collect evidence" (talk transcript: https://prepublish.ai/youtube-transcript/NjoZoUm85x0). Principle *build-the-lever*: a CLI uses less context than ad-hoc scripts and humans can rerun it.
**Template:**
```
control-<app> launch [--data-dir DIR] [--port N]   # prints READY line
control-<app> doctor                               # read-only: up, right build, our port, auth ok
control-<app> browser click --role button --name "Save"
control-<app> cli -- <app command>
control-<app> snapshot --aria --path artifacts/<feature>/x.txt
control-<app> screenshot --path artifacts/<feature>/x.png
control-<app> stop                                 # kills only what it started
```
**Proof:** from an empty data dir: launch → doctor exit 0 → one drive → artifact exists → stop → artifact still exists.

## 4. verify-<app> skill
**What:** `.cursor/skills/verify-<app>/SKILL.md` with frontmatter and sections Launch, Doctor, Drive, Evidence, Cleanup, Helpers, grounded in real commands and selectors (pstack `create-verification-skill`).
**Why:** "Every serious project needs a scripted way to drive the real app and prove behavior" (`create-verification-skill`). Lauren: verification is infrastructure, and without it every autonomous agent hands the problem back to a human (The Neuron, Lesson #1).
**Template:**
```md
---
name: verify-<app>
description: Drive <app>'s <web UI/CLI> like a user to prove behavior. Use before claiming any user-facing change works.
---
## Launch   <exact cmd>, ready when "<log line>"; from empty data dir incl. migrations/seed
## Doctor   control-<app> doctor
## Drive    see features/README.md; prefer ARIA/data-attrs/prompt strings
## Evidence real user path, action + resulting state, side effects (DB row/file), saved to artifacts/<feature>/
## Cleanup  stop what you started; never kill by process name; keep artifacts
## Helpers  scripts/control-<app> (executable, usage above)
```
**Proof:** `create-verification-skill` step 4: run its own instructions end to end once and confirm evidence survives cleanup. Re-check with `maintain-verification-skill` (outcome clean/changed/blocked, at most 1 PR). Lauren recommends running maintenance at least daily (The Neuron, Lesson #2). For Jerome that becomes a routine only if he approves one.

## 5. Feature map
**What:** `features/README.md` (baseline preconditions, driving conventions, proof rules) plus one file per user-facing feature. Each file has a title + paragraph, and four H2 sections: Sub-features (IDs), How to get to it (user POV), Driving it with control-<app> (Preconditions, then action → exact command → observable result), Gotchas.
**Why:** Lauren calls it "materialized memory": a compact index of what exists now so agents don't rediscover the product every run (The Neuron, Lesson #2). It's what ties the driver CLI to real features.
**Template:** copy pstack `create-verification-skill/references/feature-map-example/` (Notes example). Seed the top 3–5 features.
**Proof:** every feature file driven live at least once. Index has no missing, extra, or dead entries. Drift found later is fixed in the map, and product bugs are reported, never papered over in docs (`maintain-verification-skill`).

## 6. Structure, type and lint rules
**What:** architecture boundaries (one owner per piece of state, internals not importable), strict types, and custom lint/check scripts whose error message names the fix.
**Why:** `correct` order: architecture → types → lint/CI check whose error names what to use instead → behavior tests → written rules last. In the interview, when something looks wrong in the morning she "reverts what looks wrong, and adds a new lint rule" (tenten write-up of the 2 Oct 2026 interview).
**Template:** strict tsconfig / mypy strict / equivalent; `scripts/check-structure.*` for import boundaries; for existing common bad patterns, "fail only when a change adds more" (ratchet).
**Proof:** each rule ships with a fixture or commit showing it fails on a real past mistake (`correct`: "Prove each new check fails on a real past mistake"). Exceptions only inline, with a reason, an expiry, and Jerome's OK.

## 7. CI gates + branch protection
**What:** CI runs `make check` (plus a smoke drive of the verify skill when feasible) on every PR. Branch protection on main: required checks, required review, no force-push.
**Why:** In Lauren's autopilot-full playbook, nothing merges without a clean verifier verdict on the exact patch and CI passing on a head freshly rebased onto trunk (pstack `poteto-mode/playbooks/autopilot-full.md`). For Jerome, Jerome's OK replaces her self-merge step.
**Template:** `.github/workflows/check.yml` with `on: pull_request` running `make check`. Branch protection set by Jerome (a settings change, so it needs his OK).
**Proof:** an init-PR commit with a deliberately failing test shows a red check, then gets removed. `gh api repos/<o>/<r>/branches/main/protection` shows the rules.

## 8. Rule → enforcer table
**What:** a table in AGENTS.md pairing every rule with what enforces it.
**Why:** `correct` "Keep the rule table": if a rule is already there and nothing enforces it, a repeat correction means fixing it at a higher level. Drop rules once their mistake can't happen anymore.
**Proof:** a script or reviewer checks that every enforcer named exists (file/lint rule/CI job).

## 9. Decisions & learnings log
**What:** (a) `.audit/<task>.tsv` per run, using pstack `show-me-your-work` format (ts, phase, decision, why, evidence, result; append-only). It stays uncommitted unless a reviewer needs the trail. (b) `docs/decisions/NNNN-title.md` short records for one-way-door choices (from `architect`/`arena`). (c) Learnings go into skills, lints, or checks via `reflect`/`correct`, not a growing prose file.
**Why:** "The trail plus the diff is what lets the human come back and trust the work" (`figure-it-out` Phase D). Overnight guide: trust comes from "a checkable finish condition, an isolated worktree or cloud agent, and a decision log you audit in the morning" (pstack docs/guide/07-overnight.md).
**Proof:** end-of-run audit: every row maps to a real action and its evidence pointer resolves (`show-me-your-work`). A different-model reviewer adds an "Attention" section.

## 10. PR template with evidence
**What:** `.github/pull_request_template.md` with fields for intent, done predicate, verification verdict (VERIFIED / NOT VERIFIED / INCONCLUSIVE), evidence links (artifacts, transcripts, SHAs), feature-map entries touched, and the reviewers' summary.
**Why:** `figure-it-out`: "Inconclusive is not a pass. Don't hide a negative." `prove-it-works`: check the real artifact, not self-reports.
**Proof:** the init PR fills in its own template.

## 11. Isolation for parallel agents
**What:** documented env vars for port, data dir, and profile so two instances can run side by side. Each worker gets its own branch/worktree (or cloud machine).
**Why:** `create-verification-skill` "Isolate". Principle *separate-before-serializing-shared-state*. Lauren prefers cloud agents per worker over laptop worktrees once verification is strong (The Neuron, Lesson #5).
**Proof:** two `control-<app> launch` runs with different `--data-dir/--port` both pass doctor at once. If that's impossible, the verify skill says so and refuses to double-drive.

## 12. Check while you build (CHARTER 33)
**What:** the builder runs the same `make check`, verify-<app> drive and reviewer checklist while authoring, before opening a PR, and pastes the result into the PR template ("Pre-review self-check" field). Any issue kind a reviewer or verifier catches twice becomes a lint rule or `scripts/check-*` that runs in `make check` and CI, with a fixture of the real past miss that it must fail on. A PR that needs 3+ review rounds gets `docs/root-cause/<pr>.md`: what was missed and which check would have caught it while building.
**Why:** CHARTER 33 (Jerome, 15 Oct 2026): review is the last line of defence, not the first check. Extends 25 and pstack `correct`.
**Proof:** the new check fails on the real miss's fixture and passes on the fix; Fleet Auditor flags any PR with 3+ review rounds and no root-cause note.

## Rollout (only when Jerome names a repo)
One init PR per repo, in this order: 1 → 2 → 7 → 3 → 4/5 → 6 → 8 → 9 → 10 → 11. Each step ends verified (`sequence-verifiable-units`). Code opens the PR and Jerome merges.

## Visual verification (required, added 13 Oct 2026)
Verification must drive a real browser and screenshot every feature at desktop and mobile widths, including interaction states (hover, focus, pressed, expanded, answered) and text/math rendering. Verifiers inspect the images, CI holds visual-regression baselines, PRs attach screenshots as evidence, and feature-map entries list their visual states.
