# R3-2024-Tournament-Q07-v10

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 3, problem 7, slide 185)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 187)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.3, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/4}\frac{1}{2^{1/4}+\sqrt{1+\tan x}}\,dx.
\]

## Solution

King's substitution \(u=\pi/4-x\) uses \(\tan(\pi/4-u)=(1-\tan u)/(1+\tan u)\). With \(s=\sqrt{1+\tan u}\) and \(a=2^{1/4}\), so that \(a^{2}=\sqrt{2}\), the partner integrand is

\[
\frac{s}{a s+a^{2}}.
\]

The sum of the original integrand \(1/(a+s)\) and this partner is \(1/a\). Therefore

\[
2I=\int_{0}^{\pi/4}\frac{1}{a}\,dx=\frac{\pi}{4a},
\]

and \(I=\pi/(8\cdot 2^{1/4})\). The answer slide prints \(\pi/(8\sqrt[4]{2})\).

## Final answer

\[
\dfrac{\pi}{8\sqrt[4]{2}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q07_v10`. SymPy checks that the integrand and its partner sum to \(2^{-1/4}\), and halves the integral of that constant from \(0\) to \(\pi/4\).
