# R3-2024-Chainlink-G3-Q02

- Problem: `sources/past/r3/2024/Chainlink_Game_3_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 2)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 3, problem 2)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 3, problem 2)
- The catalog row is not changed.

## Problem

\[
\int_{-1}^{\infty}e^{-x^{2}}(5x^{4}-2x^{6})\,dx.
\]

## Solution

The integrand is a product-rule derivative:

\[
\frac{d}{dx}\bigl(x^{5}e^{-x^{2}}\bigr)=e^{-x^{2}}(5x^{4}-2x^{6}).
\]

The boundary term at infinity vanishes, and the value at the lower limit is \((-1)^{5}e^{-1}\). The integral is \(1/e\).

## Final answer

\[
\dfrac{1}{e}.
\]

## SymPy self-check

SymPy differentiates \(x^{5}e^{-x^{2}}\) to \(e^{-x^{2}}(5x^{4}-2x^{6})\) and evaluates the limit from \(-1\) to \(\infty\) as \(e^{-1}\).
