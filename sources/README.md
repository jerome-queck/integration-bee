# Official sources mirror

Upstream: https://integration.soc.srcf.net/

## Reference copies

The PDFs in this directory and under `past/` are committed reference copies. `Resource_pack.zip`, `index.html`, and `pastcomp.html` stay untracked. `fetch.sh` can still verify the checksums in `sha256sums`.

```bash
./sources/fetch.sh
```

Checksums in `sha256sums` are SHA-256 of the copies pulled on 2026-10-24 in Asia/Singapore.

| File | Upstream |
|---|---|
| `UK_University_Integration_Bee_Syllabus.pdf` | `/UK_University_Integration_Bee_Syllabus.pdf` |
| `UK_University_Integration_Bee_Techniques_Guide.pdf` | `/UK_University_Integration_Bee_Techniques_Guide.pdf` |
| `Integration_Competition_Sample_problems.pdf` | `/Integration_Competition_Sample_problems.pdf` |
| `Virtual_integration_competition_sample_hints.pdf` | `/Virtual_integration_competition_sample_hints.pdf` |
| `Integration_bee_sample_problems_answers.pdf` | `/Integration_bee_sample_problems_answers.pdf` |
| `UK_University_integration_bee_sample_problems_solutions.pdf` | `/UK%20University%20integration%20bee%20sample%20problems%20solutions.pdf` |
| `Resource_pack.zip` | `/Resource%20pack.zip` |
| `Formula_sheet.pdf` | inside Resource pack |
| `index.html` / `pastcomp.html` | `/` and `/pastcomp.html` |
| `past/r1/YYYY/*.pdf` | Resource pack `Round 1/` |
| `past/r2/YYYY/*.pdf` (+ `uk/`/`sg/` for 2025) | Resource pack `Round 2/` |
| `past/r3/YYYY/*.pdf` | Resource pack `Round 3/` |

Committed indexes (repo root `past/`): `past/index.md`, `past/inventory.json`, `past/README.md`.

## User-supplied (committed)

| Path | Note |
|---|---|
| `user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf` | Yuepeng Alex Yang, 2nd Ed |
| `user/yang-topics-inventory.md` | Topic ids 1.1–6.9 |
| `user/sha256sums` | Hash of Yang PDF |

See `../syllabus-map.md` for Yang ↔ official map.
