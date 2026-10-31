# C1: copied worked fields

Re-extracted every `worked_solution_origin: pdf_copy` row in `problems/records.jsonl` (193 rows) from the solution PDFs under `sources/`. A row is kept only when the printed integrand and that problem's solution block share a match that no other block in the same PDF matches as well. Otherwise `new_worked` is null.

The sidecar was built while lane L1 owned `problems/records.jsonl`. It was applied after the L1 merge (#119, d60f03a).

## Counts

| Outcome | Rows |
|---|---:|
| Examined | 193 |
| Verified extract (`new_worked` set) | 183 |
| Cleared (`new_worked` null) | 10 |
| Extract identical to the old copied field | 0 |

`apply.py` on a copy of the current catalog leaves **183** `pdf_copy` rows and sets the 10 cleared rows to `worked_solution_origin: missing` with `worked_solution_plain: null`. `verify/problem_catalog.py` sets `EXPECTED_PDF_COPY = 183`, the live `pdf_copy` count after the apply. The check is still an exact count.

| Source PDF | Extracts |
|---|---:|
| `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` | 92 |
| `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` | 40 |
| `sources/past/r2/2024/Solutions_R2_2024_UK_University_Integration_Bee.pdf` | 30 |
| `sources/past/r1/2024/Solutions_2024_Round_1_UK_University_Integration_Bee_Solutions.pdf` | 7 |
| `sources/past/r1/2023/2023_Round_1_Worked_Answers_UK_University_Integration_Bee.pdf` | 5 |
| `sources/past/r1/2020/2020_Virtual_Worked_Answers_UK_University_Integration_Bee.pdf` | 3 |
| `sources/past/r1/2025/2025_Round_1_Solutions.pdf` | 3 |
| `sources/past/r1/2022/Solutions_2022_R1_UK_University_Integration_Bee.pdf` | 2 |
| `sources/past/r1/2021/Solutions_2021_UK_University_Integration_Bee_Round_1.pdf` | 1 |

Tournament aliases of one printed integral share one extract (32 groups, 92 rows). No chainlink game shares another game's text. No row is labelled impossible. Answer fields are not changed.

## Cleared (no verified match)

These ten pack notes say the worked source is a derivation in the note and that the sheet prints only the final value. Searching the solutions PDF named on the catalog row does not find a statement that matches the integrand, so the copied field is cleared.

| Id | Why |
|---|---|
| `R1-2022-MIT-TB-Q02`, `R1-2022-MIT-TB-Q04` | 2022 main solutions PDF does not restate these MIT tiebreaker integrals |
| `R1-2022-Oxford-Q02`, `R1-2022-Oxford-Q04` | same, for the Oxford paper |
| `R1-2022-TB2022-Q02`, `R1-2022-TB2022-Q04` | same, for the tiebreaker paper |
| `R3-2024-TB1-Q01`, `R3-2024-TB2-Q01`, `R3-2024-TB3-Q01`, `R3-2024-TB4-Q01` | tiebreaker sheets print the final; the chainlink solutions PDF does not match |

The main 2022 paper's own Q02 and Q04 stay, matched to problems 2 and 4 of `Solutions_2022_R1_UK_University_Integration_Bee.pdf`.

## Official worked text kept where the printed answer is wrong

`R3-2024-Tournament-Q04-v10`, `v11`, and `v12` match section 4.2 problem 1, PDF page 15, of the tournament solutions. The extract is that official writeup, including the printed final \(\pi/2^{m-2n}\). It is not replaced with the catalog's derived value. The three ids share one sha256.

`R1-2024-Q01` stays `pdf_copy` (problem 1, page 2 of the 2024 Round 1 solutions), so the catalog pin on that worked solution still holds.

## Match check

`extract.py` runs `pdftotext -raw` on each solutions PDF and splits it into section/question blocks (Round 1 problem numbers, 2024 group and relay numbers, chainlink games 1–5, tournament fight sections such as `4.2 Fight 2`). The integrand is `integrand_plain`. A block is accepted only when its problem statement is the unique best match in that PDF: a common substring of length at least 8, the whole integrand, or a core similarity of at least 0.84 after dropping the catalog's "Game N" label and the solution's problem number. `sha256` is the SHA-256 of the UTF-8 `new_worked` string. Cleared rows have `sha256: null`.

`page` is the PDF page of the problem number, or a range when the solution continues. `question` includes the section (`Game 2 problem 1`, `4.2 Fight 2 problem 1`, `relay 5`, `problem 4`).

## Apply

```bash
python3 /workspace/tasks/ib-audit-2026-10-31/c1/apply.py \
  problems/records.jsonl -o /tmp/records.c1.jsonl
```

`--in-place` overwrites the given file. The script checks each `sha256` before writing. It sets `worked_solution_plain`, `worked_solution_origin`, and `worked_solution_latex` (null) and leaves every other field, including section-B answer corrections, unchanged. A temp-file apply changed 193 lines, left 183 `pdf_copy` rows, and was idempotent.

## Applied

All 193 rows are applied in one change on top of #119: 183 re-extracted, 10 cleared to `missing`. An earlier part-1 branch (`audit-c1-worked`, 185 rows) deferred eight rows that sat on or next to lines L1 edited: R1-2020-Q24, R1-2024-Q01, R1-2024-Q16, R2-2024-Relay-Q19, R2-2024-Relay-Q20, R3-2024-TB2-Q01, R3-2024-TB3-Q01, R3-2024-TB4-Q01. L1 changed only notes and answer fields on those rows, never the worked fields, so each sidecar extract still matches its printed integrand and they are included here. The 185 part-1 rows are identical to that branch.
