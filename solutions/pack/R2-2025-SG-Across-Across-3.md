# R2-2025-SG-Across-Across-3

## Sources and scope

- Original clue, visually read: `sources/past/r2/2025/sg/2025_R2_Crossnumber_across_SG.pdf`, p.2, A3.
- Completed grid, visually read: `sources/past/r2/2025/sg/2025_R2_Crossnumber_Markers_grid.pdf`, p.3, ANSWERS grid.
- Shared certificate: `verify/pack_grid_2025.py`, A3.

The SG catalog represents only A3. Its answer is the one-key map `{3:2026}`,
with the printed full-grid lattice and crossing context; a bare scalar 2026
is not the grid answer contract. The SG clues and completed lattice agree
with the UK copies. The full Across transcript is in
`solutions/pack/R2-2025-UK-Across-Across-3.md`.

## Derivation

The original uses ceilings. Write
\(A=\int_2^5 f\), \(B=\int_2^6 f\), and \(p=B-A=\int_5^6 f\).
The function is nonnegative, \(p\) is a positive perfect number, and
\(A^2+B^2=1076\). Hence \(p^2\le1076\), so \(p\le32\).
The only perfect numbers in this finite interval, checked by summing proper
divisors, are 6 and 28. The nonnegative solution is
\[
A=\frac{\sqrt{2152-p^2}-p}{2},\qquad B=A+p.
\]

- For \(p=6\), \((A,B)=(20,26)\).
- For \(p=28\), \((A,B)=(\sqrt{342}-14,\sqrt{342}+14)\), giving
  ceilings \((5,33)\). The first is not a two-digit prefix, so this case
  cannot form the required four-digit number.

Thus the map is `{3:2026}`. A nonnegative witness function is \(20/3\)
on \([2,5]\), followed by 6 on \((5,6]\). The certificate uses finite
divisor enumeration and exact algebraic ceilings, and agrees with the
marker grid. All four digits occur in the shared lattice at the printed A3
start, row 3 column 4 when using one-based coordinates.

## Verification

The A3 thunk passes below the unchanged 20-second timeout. The shared grid
contract rejects a changed entry, an empty map, a bare integer, and inconsistent
crossing context. It does not assert a scalar integral equals 2026.
