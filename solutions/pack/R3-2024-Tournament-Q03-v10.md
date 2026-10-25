# R3-2024-Tournament-Q03-v10

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 1, problem 3, slide 163)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 165)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.1, problem 3)
- The catalog row is not changed.

## Problem

\[
\lim_{n\to\infty}n\int_{0}^{\pi/4}\tan^{n}x\,dx.
\]

## Solution

Write \(I_{n}=\int_{0}^{\pi/4}\tan^{n}x\,dx\). Then

\[
I_{n}+I_{n+2}=\int_{0}^{\pi/4}\tan^{n}x\,(1+\tan^{2}x)\,dx=\left[\frac{\tan^{n+1}x}{n+1}\right]_{0}^{\pi/4}=\frac{1}{n+1},
\]

because the integrand is the derivative of \(\tan^{n+1}x/(n+1)\). On \((0,\pi/4]\) one has \(0<\tan x\le 1\), so \(I_{n}\) decreases in \(n\). Therefore

\[
\frac{1}{n+1}=I_{n}+I_{n+2}\le 2I_{n}\le I_{n}+I_{n-2}=\frac{1}{n-1}.
\]

Multiplying through by \(n/2\) squeezes \(n I_{n}\) to \(1/2\). The answer slide prints \(1/2\).

## Final answer

\[
\dfrac{1}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q03_v10`. SymPy differentiates \(\tan^{n+1}x/(n+1)\) and checks that the endpoint difference is \(1/(n+1)\).
