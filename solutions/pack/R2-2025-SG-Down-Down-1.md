# R2-2025-SG-Down-Down-1

## Sources and scope

- Original clue, visually read: `sources/past/r2/2025/sg/2025_R2_Crossnumber_Down_SG.pdf`, p.2, D1.
- Completed grid, visually read: `sources/past/r2/2025/sg/2025_R2_Crossnumber_Markers_grid.pdf`, p.3, ANSWERS grid.
- Shared certificate: `verify/pack_grid_2025.py`, D1.

The SG catalog represents D1 alone. Its answer is the one-key map `{1:422}`,
not a bare scalar. The full lattice supplies the crossings. Both the clue
and the completed grid agree with the UK copies; the complete Down
transcript is in `solutions/pack/R2-2025-UK-Down-Down-1.md`.

## Derivation and the outer divisor condition

The original asks for **a divisor of five times the integral**:
\[
5\int_{15}^{80}\sqrt{\sqrt{2x-2\sqrt{x^2-1}}+\sqrt{x-1}}\,dx.
\]
For \(x\ge15\),
\[
\sqrt{2x-2\sqrt{x^2-1}}=\sqrt{x+1}-\sqrt{x-1},
\]
because the right side is nonnegative and its square is the radicand.
The next radical thus reduces the integrand to \((x+1)^{1/4}\). An
antiderivative is \(\tfrac45(x+1)^{5/4}\), giving
\[
5I=4(81^{5/4}-16^{5/4})=4(243-32)=844.
\]
The marker's 422 is a divisor of 844. In fact the three-digit positive
divisors are 211, 422, and 844; A3 supplies the last digit 2 through their
crossing, selecting 422. The integral itself is \(844/5\), not 422.

The certificate checks the radical identity, positive branch on the whole
interval, derivative, endpoint powers, and divisibility. The shared grid
contract checks the printed map and lattice, including the A3 crossing.

## Verification

The D1 thunk passes below the unchanged 20-second timeout. Wrong digits,
an empty map, a bare scalar, and changed crossing data fail the shared
contract. The original outer divisor condition is preserved.
