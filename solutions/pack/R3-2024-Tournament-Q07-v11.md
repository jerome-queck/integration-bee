# R3-2024-Tournament-Q07-v11

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 3, problem 7, answer slide 187)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 187)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.3, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 187 prints the final value of Battle 4, Fight 3, problem 7:

\[
\int_{0}^{\pi/4}\frac{1}{2^{1/4}+\sqrt{1+\tan x}}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q07-v10`.

## Solution

King's substitution \(u=\pi/4-x\), with \(s=\sqrt{1+\tan u}\) and \(a=2^{1/4}\), produces the partner \(s/(as+a^{2})\). That partner and \(1/(a+s)\) sum to \(1/a\), so

\[
2I=\int_{0}^{\pi/4}a^{-1}\,dx=\frac{\pi}{4a}
\]

and \(I=\pi/(8\sqrt[4]{2})\). Slide 187 prints that value.

## Final answer

\[
\dfrac{\pi}{8\sqrt[4]{2}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q07_v11`. That check runs the partner-sum identity for `R3-2024-Tournament-Q07-v10`.
