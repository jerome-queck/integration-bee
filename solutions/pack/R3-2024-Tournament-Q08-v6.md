# R3-2024-Tournament-Q08-v6

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 3, problem 8, slide 141)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 143)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.3, problem 2)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\left(x^{e}(e^{x}+e^{-x})+x^{e-1}\bigl(e^{x+1}-e^{1-x}\bigr)\right)dx.
\]

## Solution

The integrand is the derivative of \(x^{e}e^{x}-x^{e}e^{-x}\). Expanding that derivative recovers both groups of terms, because \(e\cdot e^{x}=e^{x+1}\) and \(e\cdot e^{-x}=e^{1-x}\). The antiderivative vanishes as \(x\to 0^{+}\) and equals \(e-e^{-1}\) at \(x=1\):

\[
e-\frac{1}{e}.
\]

The answer slide prints \(e-1/e\).

## Final answer

\[
e-\dfrac{1}{e}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q08_v6`. SymPy differentiates \(x^{e}e^{x}-x^{e}e^{-x}\) and evaluates it from \(0\) to \(1\).
