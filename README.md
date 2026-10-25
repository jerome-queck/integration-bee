# Integration Bee

Public study pack for the UK University Integration Bee.

A learner talks to the companion. The companion reads `.cursor/skills/integration-bee-companion/SKILL.md` and sends a JSON turn to `scripts/control-integration-bee`. The learner does not run commands.

## Start

The learner talks to the companion and does not run the CLI. The companion reads `.cursor/skills/integration-bee-companion/SKILL.md` and writes one JSON turn.

```bash
scripts/control-integration-bee turn apply --file turn.json --format json
```

Begin with `{"kind":"aptitude"}`. The first integral is a unit drill. The learner sends written working. The companion marks it with `{"kind":"mark",...}`. A correct mark opens one contest integral from the catalog. That contest verdict stores an attempt and does not tick a node.

When the result phase is `proposing`, ask which nodes in `coach.offer` to skip. Send `{"kind":"confirm","nodes":[...]}` with only those ids. An empty list skips nothing and declines the offer, so those ids are not offered again. A confirm before that offer, or a confirm that names an id outside it, exits 2 and writes nothing.

After confirm, continue with `{"kind":"teach"}`. `coach.detail`, `coach.approach`, `coach.kind`, and `coach.volume` are the dosage for `coach.next_node`. A miss moves that dosage back toward a worked example. Send `{"kind":"aptitude"}` again only for another placement probe. The learner does not finish every Round 1 probe before coaching.

`{"kind":"cover","full":true}` turns full coverage on and puts confirmed skips back in the coach queue. The default leaves them out. The mock still needs every Round 1 node `solid`.

## How it works

`turn apply` is the only writer of learner state. Kinds are empty, teach, mark, mock-start, mock-finish, aptitude, confirm, and cover. `confirm` is the only new writer of `skipped`, and only for ids in the open offer. `progress tick` can still set `skipped` by hand.

The session file is `session.json` in the data directory. One replace holds the phase, the skip offer, declined ids, the coverage flag, and the per-node dosage. Set `IB_DATA_DIR`, or leave the files in `trackers/live`. `progress.local.json` and `trackers/live/` are gitignored.

`problems/records.jsonl` is the contest catalog. `problems list` and `problems select` hide answers. A `manual` row is a cited answer the companion judges. An `unchecked` row has no printed answer and must not be invented. Pack rows are not SymPy-checked. Unit drills are.

`make check` runs `verify/run.sh`. That script drives the turn contract, including aptitude, confirm, and cover.

## Learner

Ask the companion for a concept, or send a photo of a solution.

## Maintainer

People changing this pack use the checks below. Learners do not.

1. Install Python 3.11 or newer, SymPy, and PyYAML with `python3 -m pip install sympy pyyaml`.
2. Run `make check` before a pull request. CI runs the same command. Details are in `AGENTS.md`.
3. The unpacked contest PDFs and the site PDFs are committed reference copies under `sources/past/` and `sources/`. The contest list is `past/inventory.json`. Do not commit `Resource_pack.zip`.
4. Teach from `units/` with the files in `templates/`.
5. The Yang Topics Guide, 2nd edition, is `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`. Attribution is in `sources/user/README.md`.
6. Contest and Yang problems are `problems/records.jsonl`. `problems list` hides answers. A mark still goes through `turn apply`.

Syllabus links are in `syllabus-map.md`. The skill tree is `skill-tree.md`.
