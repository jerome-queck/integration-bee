# R3-2024-Tournament-Q05-v5

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 2, problem 5, answer slide 78)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 78)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.2, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 78 prints the final value of Battle 2, Fight 2, problem 5:

\[
\int_{0}^{1}\frac{\ln x\,(2x-1)}{\sqrt{x-x^{2}}}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q05-v4`.

## Solution

The solutions PDF integrates by parts. The factor \((2x-1)/\sqrt{x-x^{2}}\) is the derivative of \(-2\sqrt{x-x^{2}}\), and the boundary term \(-2\ln x\sqrt{x-x^{2}}\) vanishes at both endpoints. The integral that remains is

\[
2\int_{0}^{1}\frac{\sqrt{x-x^{2}}}{x}\,dx.
\]

The substitution \(x=\sin^{2}u\) gives \(dx=2\sin u\cos u\,du\) and

\[
2\int_{0}^{\pi/2}\frac{\sin u\cos u}{\sin^{2}u}\cdot 2\sin u\cos u\,du=4\int_{0}^{\pi/2}\cos^{2}u\,du=\pi.
\]

The answer slide prints \(\pi\).

## Final answer

\[
\pi.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q05_v5`. That check runs `check_r3_2024_tournament_q05_v4` for `R3-2024-Tournament-Q05-v4`. SymPy differentiates \(-2\sqrt{x-x^{2}}\) and evaluates \(4\int_{0}^{\pi/2}\cos^{2}u\,du=\pi\).
