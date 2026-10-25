# R3-2024-Tournament-Q07-v9

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 3, problem 7, answer slide 138)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 138)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.3, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 138, not the integral. Slide 138 is the answer reveal for Battle 3, Fight 3, problem 7:

\[
\int_{0}^{\infty}\cos\left(x^{2}+\frac{1}{x^{2}}\right)dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q07-v7`.

## Solution

The argument of the cosine splits as

\[
x^{2}+\frac{1}{x^{2}}=\left(x-\frac{1}{x}\right)^{2}+2.
\]

The solutions PDF applies Glasser's master theorem to replace \(x-1/x\) by \(x\), and uses that the integrand of the resulting cosine is even:

\[
\int_{0}^{\infty}\cos\left(x^{2}+\frac{1}{x^{2}}\right)dx=\frac12\int_{-\infty}^{\infty}\cos(x^{2}+2)\,dx=\int_{0}^{\infty}\bigl(\cos 2\cos(x^{2})-\sin 2\sin(x^{2})\bigr)dx.
\]

The Fresnel integrals \(\int_{0}^{\infty}\cos(x^{2})\,dx\) and \(\int_{0}^{\infty}\sin(x^{2})\,dx\) are both \(\sqrt{2\pi}/4\), so the value is

\[
\frac{\sqrt{2\pi}}{4}(\cos 2-\sin 2).
\]

The answer slide prints the same expression.

## Final answer

\[
\dfrac{\sqrt{2\pi}}{4}(\cos 2-\sin 2).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q07_v9`. That check runs `check_r3_2024_tournament_q07_v7` for `R3-2024-Tournament-Q07-v7`. SymPy checks \(x^{2}+1/x^{2}=(x-1/x)^{2}+2\) and evaluates both Fresnel integrals as \(\sqrt{2\pi}/4\).
