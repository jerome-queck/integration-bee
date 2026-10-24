# Integration Bee

Public study pack for the UK University Integration Bee.

A learner talks to the companion. The companion reads `.cursor/skills/integration-bee-companion/SKILL.md` and sends a JSON turn to `scripts/control-integration-bee`. The learner does not run commands.

## Learner

Ask the companion for a concept, or send a photo of a solution.

## Maintainer

People changing this pack use the checks below. Learners do not.

1. Install Python 3.11 or newer and SymPy with `python3 -m pip install sympy`.
2. Run `make check` before a pull request. CI runs the same command. Details are in `AGENTS.md`.
3. Official contest PDFs stay out of git. `sources/fetch.sh` downloads them. The committed list is `past/inventory.json`.
4. Teach from `units/` with the files in `templates/`.
5. The Yang Topics Guide, 2nd edition, is `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`. Attribution is in `sources/user/README.md`.

Syllabus links are in `syllabus-map.md`. The skill tree is `skill-tree.md`.
