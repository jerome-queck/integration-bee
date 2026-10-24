# Problem catalog

Contest and Yang integrals live in `problems/records.jsonl`. The file is public study material. It is not learner state.

The import copies extract fields and does not add a SymPy answer. `verify` stays `manual` when the extract cites an answer, and `unchecked` when it does not. Two Yang examples already print an equality. The other Yang practice rows stay unanswered.

`problems list`, `problems show`, and `problems select` only read that file. A mark of a manual row goes through `turn apply` and the same attempt writer as a drill. The lossy integrand is not sent to SymPy. An unanswered row cannot be marked.

Unit drills in `verify/drills_unit*.json` stay the SymPy-checked concept drills. `trackers/catalog.json` stays the skill-tree id list.
