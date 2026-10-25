# R3-2024-Tournament-Q09-v12

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 3, problem 9, answer slide 197)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 197)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.3, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 197, not the integral. Slide 197 is the answer reveal for Battle 4, Fight 3, problem 9:

\[
\int_{1}^{3}\frac{\ln x}{x^{2}+3}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q09-v10`.

## Solution

Split the integral at \(\sqrt{3}\). In the piece from \(\sqrt{3}\) to \(3\), set \(x=3/u\). The limits swap back to \(1\) and \(\sqrt{3}\), and the integrand becomes \((\ln 3-\ln u)/(u^{2}+3)\). Adding the two pieces cancels \(\ln x\) and leaves

\[
\ln 3\int_{1}^{\sqrt{3}}\frac{1}{u^{2}+3}\,du=\frac{\ln 3}{\sqrt{3}}\left[\arctan\frac{x}{\sqrt{3}}\right]_{1}^{\sqrt{3}}.
\]

The arctangents are \(\pi/4\) and \(\pi/6\), so the value is

\[
\frac{\ln 3}{\sqrt{3}}\left(\frac{\pi}{4}-\frac{\pi}{6}\right)=\frac{\pi\ln 3}{12\sqrt{3}}.
\]

The answer slide prints \(\pi\ln 3/(12\sqrt{3})\).

## Final answer

\[
\dfrac{\pi\ln 3}{12\sqrt{3}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q09_v12`. That check runs `check_r3_2024_tournament_q09_v10` for `R3-2024-Tournament-Q09-v10`. SymPy evaluates \(\int_{1}^{\sqrt{3}}dx/(x^{2}+3)=\pi/(12\sqrt{3})\) and multiplies by \(\ln 3\).
