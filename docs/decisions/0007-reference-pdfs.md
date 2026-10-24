# Reference PDFs

The unpacked contest PDFs under `sources/past/` and the site PDFs under `sources/` are committed reference copies. `Resource_pack.zip` stays untracked.

This change does not copy problem text, solution text, or technique notes out of those PDFs. A later wave puts that text in repo files. Teaching text stays in the unit files.

`sources/fetch.sh` can still verify `sources/sha256sums`. A missing reference PDF leaves `official_pdfs=missing` and does not change the doctor exit code.
