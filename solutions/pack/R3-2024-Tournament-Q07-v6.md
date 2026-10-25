# R3-2024-Tournament-Q07-v6

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 3, problem 7, answer slide 89)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 89)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.3, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 89, not the integral. Slide 89 is the answer reveal for Battle 2, Fight 3, problem 7:

\[
\int_{3}^{4}\frac{x-\sqrt{7x-x^{2}}}{2x-7}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q07-v4`.

## Solution

The interval \([3,4]\) is symmetric about \(7/2\). King's substitution \(x\mapsto 7-x\) leaves the interval fixed and replaces the integrand by

\[
\frac{(7-x)-\sqrt{7x-x^{2}}}{7-2x}.
\]

The sum of the original integrand and this partner is \(1\), so

\[
2I=\int_{3}^{4}1\,dx=1
\]

and \(I=1/2\). The answer slide prints \(1/2\).

## Final answer

\[
\dfrac{1}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q07_v6`. That check runs `check_r3_2024_tournament_q07_v4` for `R3-2024-Tournament-Q07-v4`. SymPy simplifies the sum of the integrand and its partner to \(1\), and integrates that sum from \(3\) to \(4\).
