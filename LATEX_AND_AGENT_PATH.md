# Jerome 24 Oct 22:59 — LaTeX + agent path

## Documents
- No Grok Bot Pages as the source of truth.
- All teaching / drill / solution docs: LaTeX → PDF.
- Shared LaTeX templates that any LLM **must** use (title page, sectioning, theorem/example/exercise environments, answer key) so design language stays consistent.

## Agent path
- Solid AGENTS.md (or equivalent) at repo root.
- One clear entry path any agent can follow: README → AGENTS.md → companion skill → main CLI → units/ → templates/.
- Progress/learning tracker remains durable state the CLI owns.

## AGENTS.md sync (Jerome 24 Oct 23:00)
- AGENTS.md always current; **automatically updated** when code changes if needed.
- Must explicitly state: feature map, agent CLI, both verifier skills, pstack skills + which to run in any scenario, other standing instructions.
- Prefer a generator or CI/pre-commit check so the file cannot silently drift.

## Design freedom (Jerome 24 Oct 23:01)
- Other template types allowed; Code/Integration Bee have full design decisions.
- Spawn as many CloudAgents / sessions as needed to finish the build.
