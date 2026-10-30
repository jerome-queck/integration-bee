# Problem catalog

Contest and Yang integrals live in `problems/records.jsonl`. The file is public study material. It is not learner state.

Current state: every Yang row is `verify: sympy`, `EXPECTED_SYMPY=948` / `EXPECTED_MANUAL=0`, and all 275 Yang rows have checked worked solutions (`worked_solution_origin` `derived`) that `verify/yang_worked_check.py` enforces in `make check`. The paragraph below is the import history.

The import copies extract fields and does not add a SymPy answer. At import, `verify` stays `manual` when the extract cites an answer, and `unchecked` when it does not. Two Yang examples already print an equality. The other Yang practice rows stay unanswered. Later exact certificates supersede that import flag for proved rows. The live counts are in [0016](0016-pack-source-holds.md): at tip `770c6e4` the resource pack is 674 SymPy / 0 manual / 0 unchecked, `EXPECTED_SYMPY=676` / `EXPECTED_MANUAL=0`, and SAMPLE is 20 SymPy / 0 manual. 0 Yang rows stay `unchecked`; with every Yang row proved, `EXPECTED_SYMPY=948`. Teaching deferred is 0.

`problems list`, `problems show`, and `problems select` only read that file. A mark of a manual row goes through `turn apply` and the same attempt writer as a drill. The lossy integrand is not sent to SymPy. An unanswered row cannot be marked.

Unit drills in `verify/drills_unit*.json` stay the SymPy-checked concept drills. `trackers/catalog.json` stays the skill-tree id list.
