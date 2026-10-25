# R3-2024-Tournament-Q08-v4

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 3, problem 8, answer slide 94)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 94)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.3, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 94 prints the final value of Battle 2, Fight 3, problem 8:

\[
\int_{1}^{\infty}\frac{1+2x\ln 2}{x\sqrt{x\cdot 4^{x}-1}}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q08-v3`.

## Solution

Set \(u=x\cdot 4^{x}-1\). Then \(u'=4^{x}(1+2x\ln 2)\) and \(u+1=x\cdot 4^{x}\). At the endpoints, \(u(1)=3\) and \(u(\infty)=\infty\). The integral becomes

\[
\int_{3}^{\infty}\frac{1}{(u+1)\sqrt{u}}\,du.
\]

The substitution \(y=\sqrt{u}\) gives \(du=2y\,dy\) and

\[
\int_{\sqrt{3}}^{\infty}\frac{2}{1+y^{2}}\,dy=2\left(\frac{\pi}{2}-\frac{\pi}{3}\right)=\frac{\pi}{3}.
\]

The answer slide prints \(\pi/3\).

## Final answer

\[
\dfrac{\pi}{3}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q08_v4`. That check runs `check_r3_2024_tournament_q08_v3` for `R3-2024-Tournament-Q08-v3`. SymPy checks \(u'=4^{x}(1+2x\ln 2)\) and the evaluation \(2(\pi/2-\pi/3)=\pi/3\).
