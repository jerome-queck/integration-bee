# Past papers pedagogy pack (all rounds)

Machine-consumable layer over official contest PDFs. Binaries live under `sources/past/` (**not committed** — run `sources/fetch.sh`).

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
  inventory.json      # machine inventory (disk truth after fetch)
  samples/            # Round-1 sample bridge (Q tags + answers_feed)
  mocks/              # timed / PDF mock metas (Round 1 first)
```

## Fetch

```bash
./sources/fetch.sh
```

Pulls homepage PDFs + `Resource pack.zip`, migrates any legacy `sources/past/YYYY/` into `r1/YYYY/`, extracts **all** Round 1/2/3 PDFs. Nested `Resource pack 2025.zip` inside the outer zip is skipped (older subset).

## Honesty rules

- Never invent contest answers. Mark from official mark-scheme / solutions PDFs only.
- `pastcomp.html` has no per-paper PDF links; the Resource pack is the sole bulk source.
- Sample Q17 typo note still applies (`samples/`).

## Chat

Jerome never opens this folder — Integration Bee bot drives Flow 2 (photo mark) and Flow 3 (timed mock) from `CHAT_FLOWS.md`. Round 1 PDF mocks are primary; Round 2/3 are available as local PDFs for later flows.
