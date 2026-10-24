# Problem catalog

`problems/records.jsonl` is the contest and Yang catalog. One JSON object per line. `scripts/import_resource_catalog.py` rewrites the file from an extract list and refuses to write when `verify/problem_catalog.py` rejects the rows.

`problems list` and `problems select` hide answers. `problems show` prints the stored record. A mark goes through `turn apply`.
