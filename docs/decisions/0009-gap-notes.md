# Gap notes

`turn apply` writes learner state only. Teaching notes are git content. The six headings in `docs/techniques/beyond-yang.md` are the only gap list. `verify/gap_index.py` is the only parser.

A mark may set `extract.gap` to one of those headings. `say` names exactly one file: the unit note for a miss with no gap, or the note on that heading. `turn apply` stores the id on the attempt. It does not write the note. A later commit updates the file `say` named. A study session does not edit a teaching note.

A correct final answer with a gap also needs `extract.method_note`. A wrong final answer stores the gap id and drops `method_note`. An unknown id, an unreadable index, or a retry that names a different id exits 2 and writes nothing. A retry of the same open answer can fill a missing id. It does not append a second attempt and it does not clear an id already stored.
