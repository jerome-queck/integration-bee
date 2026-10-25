# R3-2024-Chainlink-G2-Q01

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 1)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 1)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{-1}^{0}5(x^{6}+x)^{4}\,dx.
\]

## Solution

The solutions PDF factors \(x^{6}+x=x(x^{5}+1)\):

\[
5(x^{6}+x)^{4}=5x^{4}(x^{5}+1)^{4}=\frac{d}{dx}\frac{(x^{5}+1)^{5}}{5}.
\]

The definite integral is \(\bigl[(x^{5}+1)^{5}/5\bigr]_{-1}^{0}=1/5\).

## Final answer

\[
\dfrac{1}{5}.
\]

## SymPy self-check

SymPy differentiates \((x^{5}+1)^{5}/5\) to \(5(x^{6}+x)^{4}\) and evaluates the antiderivative from \(-1\) to \(0\) as \(1/5\).
