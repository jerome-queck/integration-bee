# R3-2024-Tournament-Q02-v4

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 1, problem 2, answer slide 62)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 62)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.1, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 62 prints the final value of Battle 2, Fight 1, problem 2:

\[
\int_{0}^{\infty}\frac{\arctan x}{x\bigl((\ln x)^{2}+1\bigr)}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q02-v3`.

## Solution

The substitution \(x=1/y\) replaces \(\arctan x\) by \(\arctan(1/x)\) and leaves the rest of the integrand unchanged. For \(x>0\),

\[
\arctan x+\arctan\frac{1}{x}=\frac{\pi}{2},
\]

so averaging the two forms gives

\[
I=\frac{\pi}{4}\int_{0}^{\infty}\frac{1}{x\bigl((\ln x)^{2}+1\bigr)}\,dx.
\]

The further substitution \(t=\ln x\) produces

\[
\frac{\pi}{4}\int_{-\infty}^{\infty}\frac{1}{1+t^{2}}\,dt=\frac{\pi}{4}\cdot\pi=\frac{\pi^{2}}{4}.
\]

The answer slide prints \(\pi^{2}/4\).

## Final answer

\[
\dfrac{\pi^{2}}{4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q02_v4`. That check runs `check_r3_2024_tournament_q02_v3` for `R3-2024-Tournament-Q02-v3`. SymPy checks that \(\arctan x+\arctan(1/x)\) is constant and equals \(\pi/2\) at \(x=1\), and evaluates \(\int_{-\infty}^{\infty}dt/(1+t^{2})=\pi\).
