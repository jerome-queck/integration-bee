# Past papers pedagogy pack (all rounds)

Machine-consumable layer over official contest PDFs. The reference copies under `sources/past/` are committed.

## Layout (locked)

```
sources/past/
  r1/YYYY/*.pdf          # Round 1 (2020–2025)
  r2/YYYY/*.pdf          # Round 2 (2021–2024)
  r2/2025/uk/*.pdf       # Round 2 2025 UK version
  r2/2025/sg/*.pdf       # Round 2 2025 Singapore version
  r3/YYYY/*.pdf          # Round 3 (2024 in current pack)
```

Committed here:

```
past/
  README.md           # this file
  index.md            # human inventory table
  inventory.json
  samples/            # Round-1 sample bridge (Q tags + answers_feed)
  mocks/              # timed / PDF mock metas (Round 1 first)
```

## Fetch

A clone already has the reference PDFs. `sources/fetch.sh` can refresh the pack and check `sources/sha256sums`.

```bash
./sources/fetch.sh
```

The script pulls the homepage PDFs and `Resource pack.zip`, moves any legacy `sources/past/YYYY/` tree into `r1/YYYY/`, and extracts the Round 1, Round 2, and Round 3 PDFs. Nested `Resource pack 2025.zip` inside the outer zip is an older subset. The script skips it.

## Honesty rules

- Never invent contest answers. Mark from official mark-scheme / solutions PDFs only.
- `pastcomp.html` has no per-paper PDF links; the Resource pack is the sole bulk source.
- Sample Q17 typo note still applies (`samples/`).

## Chat

Jerome never opens this folder — Integration Bee bot drives Flow 2 (photo mark) and Flow 3 (timed mock) from `CHAT_FLOWS.md`. Round 1 PDF mocks are primary; Round 2/3 are available as local PDFs for later flows.
