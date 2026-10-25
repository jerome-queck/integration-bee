# R3-2024-Chainlink-G4-Q02

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 2)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 2)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 2)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{1+\sqrt{1-x^{2}}}{\sqrt{1+x}+\sqrt{1-x}}\,dx.
\]

## Solution

Rationalising the denominator multiplies the numerator and denominator by \(\sqrt{1+x}-\sqrt{1-x}\). The solutions PDF reduces the result to

\[
\frac12\int_{0}^{1}\bigl(\sqrt{1+x}+\sqrt{1-x}\bigr)\,dx=\frac13\Bigl[(1+x)^{3/2}-(1-x)^{3/2}\Bigr]_{0}^{1}=\frac{2\sqrt{2}}{3}.
\]

## Final answer

\[
\dfrac{2\sqrt{2}}{3}.
\]

## SymPy self-check

For \(x>0\), SymPy simplifies \(\sqrt{1-x^{2}}\) to \(\sqrt{1-x}\sqrt{1+x}\). Expanding the rationalised numerator after that replacement gives \(x\bigl(\sqrt{1+x}+\sqrt{1-x}\bigr)\), so dividing by \(2x\) leaves \(\frac12(\sqrt{1+x}+\sqrt{1-x})\). Differentiating \(\frac13\bigl((1+x)^{3/2}-(1-x)^{3/2}\bigr)\) returns that reduced integrand, and the endpoints give \(2\sqrt{2}/3\).
