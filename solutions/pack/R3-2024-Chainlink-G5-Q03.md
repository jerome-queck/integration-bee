# R3-2024-Chainlink-G5-Q03

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 3)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 3)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 3)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{1}{1+\sqrt{\dfrac{1-x+\sqrt{x}}{x+\sqrt{1-x}}}}\,dx.
\]

## Solution

King's substitution \(x\mapsto 1-x\) replaces the fraction under the square root by its reciprocal. If \(I\) is the integral and \(r(x)\) is that square root, then

\[
I=\int_{0}^{1}\frac{r(x)}{r(x)+1}\,dx
\]

as well. Adding the two copies gives \(2I=\int_{0}^{1}1\,dx=1\), so \(I=1/2\).

## Final answer

\[
\dfrac{1}{2}.
\]

## SymPy self-check

SymPy checks that \(\dfrac{1-x+\sqrt{x}}{x+\sqrt{1-x}}\) and the same expression at \(1-x\) are reciprocals. For \(r>0\), \(1/(1+r)+r/(1+r)=1\).
