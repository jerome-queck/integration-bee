# R3-2024-Chainlink-G4-Q05

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 5)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 5)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 5)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[
\int_{0}^{\pi/4}\frac{\cos(2x)}{-\ln(\tan x)\,\cos^{4}x}\,dx.
\]

## Solution

Set \(u=-\ln(\tan x)\), so \(x=\arctan(e^{-u})\) and \(u\) runs from \(\infty\) down to \(0\). Then \(\cos x=1/\sqrt{1+e^{-2u}}\) and

\[
dx=-\frac{e^{-u}}{1+e^{-2u}}\,du,\qquad\frac{\cos(2x)}{\cos^{4}x}=(1+e^{-2u})(1-e^{-2u}).
\]

The factors of \(1+e^{-2u}\) cancel, the limits flip, and the integral becomes

\[
\int_{0}^{\infty}\frac{e^{-u}-e^{-3u}}{u}\,du=\ln 3.
\]

## Final answer

\[
\ln 3.
\]

## SymPy self-check

The gate checks the tangent substitution and expresses the reduced logarithmic quotient as an integral of the nonnegative power kernel. SymPy evaluates the two integrals to the printed logarithm.
