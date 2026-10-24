# Integration Bee

Public study pack for the UK University Integration Bee.

A learner talks to the companion. The companion reads `.cursor/skills/integration-bee-companion/SKILL.md` and sends a JSON turn to `scripts/control-integration-bee`. The learner does not run commands.

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
