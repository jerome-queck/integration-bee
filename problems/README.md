# Problem catalog

`problems/records.jsonl` is the contest, Yang, and sample catalog. One JSON object per line. Sample rows use `round` `sample` and `source` `uk_sample`. Their worked notes are `solutions/sample/`. `scripts/import_resource_catalog.py` rewrites the file from an extract list, keeps existing sample rows, and refuses to write when `verify/problem_catalog.py` rejects the rows.

`problems list` and `problems select` hide answers. `problems show` prints the stored record. A mark goes through `turn apply`.
