# R3-2024-Tournament-Q01-v5

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 1, problem 1, answer slide 57)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 57)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.1, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 57 prints the final value of Battle 2, Fight 1, problem 1:

\[
\int_{1}^{e}\frac{x\ln x}{(1+\ln x)^{3}}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q01-v4`.

## Solution

Set \(u=1+\ln x\). Then \(x=e^{u-1}\), \(dx=x\,du\), and \(\ln x=u-1\). The limits change from \(x=1\) to \(x=e\) into \(u=1\) to \(u=2\), and the integral becomes

\[
e^{-2}\int_{1}^{2}\frac{e^{2u}(u-1)}{u^{3}}\,du.
\]

The integrand is the derivative of \(e^{2u}/(2u^{2})\):

\[
e^{-2}\left[\frac{e^{2u}}{2u^{2}}\right]_{1}^{2}=\frac12\left(\frac{e^{2}}{4}-1\right).
\]

The answer slide prints \(\frac12(e^{2}/4-1)\).

## Final answer

\[
\dfrac{1}{2}\left(\dfrac{e^{2}}{4}-1\right).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q01_v5`. That check runs `check_r3_2024_tournament_q01_v4` for `R3-2024-Tournament-Q01-v4`. SymPy differentiates \(e^{2u}/(2u^{2})\) and evaluates the definite integral.
