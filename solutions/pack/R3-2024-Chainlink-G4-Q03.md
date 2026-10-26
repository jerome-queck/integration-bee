# R3-2024-Chainlink-G4-Q03

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf`, PDF page 1, problem 3.
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf`, PDF page 5, Game 4, problem 3.
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, PDF page 14, Game 4, problem 3.
- The original, mark, and worked pages have been visually checked; all agree with this reading and value.

## Problem

\[
\int_{1}^{\infty}\frac{(-1)^{\lceil x\rceil}}{\sqrt{\lfloor x\rfloor\lceil x\rceil}\bigl(\sqrt{\lceil x\rceil}-\sqrt{\lfloor x\rfloor}\bigr)}\,dx.
\]

## Solution

On \((n,n+1)\) the floor is \(n\) and the ceiling is \(n+1\). Rationalising \(\sqrt{n+1}-\sqrt{n}\) produces

\[
\sum_{n=1}^{\infty}(-1)^{n+1}\left(\frac{1}{\sqrt{n}}+\frac{1}{\sqrt{n+1}}\right).
\]

Pairing \(n=2k-1\) with \(n=2k\) leaves the telescoping difference \(1/\sqrt{2k-1}-1/\sqrt{2k+1}\). The partial sum through \(k=m\) is \(1-1/\sqrt{2m+1}\), and the series sums to \(1\).

More generally, the sum through every integer \(N\) is
\[
1+\frac{(-1)^{N+1}}{\sqrt{N+1}}.
\]
Its error is at most \(1/\sqrt{N+1}\). A noninteger upper endpoint adds only a fraction of one constant interval, bounded in magnitude by \(1/\sqrt{N+1}+1/\sqrt{N+2}\), which also tends to zero. This proves the improper integral, including arbitrary upper endpoints. The undefined values at the integer endpoints may be assigned arbitrarily without changing the interval integrals.

## Final answer

\[
1.
\]

## SymPy self-check

`verify/pack_hard_floor.py` checks the exact original integrand and bounds, the floor/ceiling interval values, rationalisation, the partial-sum recurrence and its initial value, and both vanishing error bounds. It does not use absolute convergence or numerical agreement.
