# How poteto says to use pstack (from @poteto on X, read 24 Oct 2026)

Source account: https://x.com/poteto (lauren)

## 10-second tutorial (her words, paraphrased)
1. Run /setup-pstack and choose your budget.
2. Put /poteto-mode in front of hard prompts that need rigor (not every tiny task).
3. When unsure which skill: /poteto-help.

## Skills she highlighted for this project
- /create-verification-skill → project-local verifier + feature map (drive the app like a user).
- /create-formal-verification-skill → formal suite (e.g. TLA+) for high-cost / low-test areas; pair with statecharts.
- /correct → when agents keep making the same mistake, fix architecture/types/lints not more prose.
- /in-your-own-words → align on goals before building.
- Engineering principles stay short; prefer lint/types/API design over long agents.md comments.
- Ban drive-by code comments that agents will copy.

## For cloud agents
- Spawn with mode/custom_mode set to poteto-mode when rigor is needed.
- Leave bots in /poteto-mode and let it pick skills.

## Integration Bee implications
- CLI + verifier + formal verifier + feature map are first-class.
- Portable markdown/scripts in the public GitHub repo; Grok Pages are a view, not the source of truth.
