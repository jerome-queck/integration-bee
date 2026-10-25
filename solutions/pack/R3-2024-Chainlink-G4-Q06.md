# R3-2024-Chainlink-G4-Q06

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 6)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 6)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 6)
- The catalog row is not changed.

## Problem

\[
\int\frac{1}{1+x^{2}}\arctan\left(\frac{4x-4x^{3}}{x^{4}-6x^{2}+1}\right)\,dx.
\]

## Solution

Let

\[
u=\arctan\left(\frac{4x-4x^{3}}{x^{4}-6x^{2}+1}\right).
\]

The solutions PDF records the derivative \(u'=4/(1+x^{2})\). The integrand is \(u\cdot u'/4\), so

\[
\int\frac{u\,u'}{4}\,dx=\frac{u^{2}}{8}+C.
\]

## Final answer

\[
\dfrac{1}{8}\arctan^{2}\left(\dfrac{4x-4x^{3}}{x^{4}-6x^{2}+1}\right)+C.
\]

## SymPy self-check

For \(x>0\), SymPy differentiates the arctangent in the integrand to \(4/(1+x^{2})\), and differentiates one eighth of its square back to the integrand.
