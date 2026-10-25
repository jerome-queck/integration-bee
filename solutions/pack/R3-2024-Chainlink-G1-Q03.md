# R3-2024-Chainlink-G1-Q03

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 3)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 3)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 3)
- The catalog row is not changed.

## Problem

\[
\int\frac{1+\ln x}{\sqrt{x^{-2x}-1}}\,dx.
\]

## Solution

Multiplying the numerator and denominator by \(x^{x}\) produces the derivative of \(\arcsin(x^{x})\):

\[
\int\frac{x^{x}(1+\ln x)}{\sqrt{1-x^{2x}}}\,dx=\arcsin(x^{x})+C.
\]

The solutions PDF also records the alternative \(-\arctan\sqrt{x^{-2x}-1}+C\). On the range where \(x^{x}\in(0,1)\) the two antiderivatives differ by the constant \(\pi/2\). The answers sheet prints both.

## Final answer

\[
\arcsin(x^{x})+C.
\]

## SymPy self-check

For \(x>0\), SymPy differentiates \(\arcsin(x^{x})\) back to \((1+\ln x)/\sqrt{x^{-2x}-1}\), and the derivative of the gap between that antiderivative and \(-\arctan\sqrt{x^{-2x}-1}\) is \(0\).
