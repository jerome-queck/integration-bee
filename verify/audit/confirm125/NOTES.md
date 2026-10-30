- 22:27 SGT: cancelled code-ibe-confirm125 at 79 rows (it had loaded pre-revision checks and was stuck on the old G2-Q08 check); resubmitted as code-ibe-confirm125-r2 (resumes, skips done rows). retest of 9 revised checks queued under heavy.
- 22:5x SGT: G2-Q08 Hurwitz check at n=10^(10^6) was too slow (13s/zeta call); replaced with n=1e3/1e6/1e12 asymptotic form; cancelled r2, submitted r3.
- 22:4x SGT: revision 3 checks (S1-Q04a depth 150, G4-Q07, Tournament-Q03, Relay-Q10); added --recheck mode (drops non-CONFIRMED rows and reruns them). Plan: after r3 finishes, submit r4 = --recheck.
- 23:1x SGT: r3 reached 124/125 (last row YANG-2.4-P09 old check hangs; 1800s row timeout). Revision 4 checks: YANG-2.4-P09, SG/UK Q21/Q13 (sinh NameError), S2-Q06a/b (60 dps), Tournament-Q06 (sin^2 split), SG/UK-Group-Q07/Q06 via Glasser master theorem. Retests of all revised checks pass. r4s0/r4s1 queued to recheck all non-CONFIRMED rows.

## Final (2026-10-30 ~23:45 SGT)
- 125/125 CONFIRMED. 0 answers changed; 0 unconfirmable. Every first-pass mismatch/error was a defect in the numeric check, not in the pack answer.
- results.tsv = final per-row result; results_pass1.tsv = first pass (r3); recheck_{0,1}.tsv = r5 recheck (2 shards, boxops); recheck_2.tsv = Relay-Q08/Q09 after revision 5.
- r4 never ran: its cmd wrapped heavy inside boxops' own heavy wrapper, so the inner admission queued behind its own outer slots (cap 2). r5 drops the inner wrapper.
- Limit/Richardson rows (Relay-Q06/Q13/Q19, Online-Q12, G1-Q08, Tournament-Q03-v10..12): each passes within its stated extrapolation error (column method, `extrap_err~`), tol set per method (1e-9 for 1/n Neville).
- Relay-Q09 is a limit N->inf: product telescopes to 1-x^(2^(N+1)), I_N = 1-1/(2^(N+1)+1) verified by quad for N=5,20,60 to <1e-30; limit 1 is exact.

## Flags (not fixed in this PR)
- answer_plain misaligned: R2-2025-UK-Group-Q04, R2-2025-UK-Group-Q09.
- answer_plain truncated: R3-2024-Chainlink-G2-Q08, R3-2024-Chainlink-G5-Q07, R3-2024-Dichotomy-S1-Q04a, R3-2024-Chainlink-G4-Q07.
- R2-2021-Relay-C01: answer depends on the arccot branch convention (confirmed under the encoding's SymPy acot branch, range (-pi/2, pi/2]; the (0, pi) convention may give a different value).
- Some rows rest on a limit/analytic argument (Glasser for SG-Group-Q07/UK-Group-Q06; telescoping for Relay-Q08/Q09); see method column.
