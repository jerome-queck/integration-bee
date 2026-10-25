# R3-2024-Chainlink-G1-Q06

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 6)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 6)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 6)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}f(x)\,dx,\quad f(x)=\begin{cases}1,&x=0.x_{1}x_{2}x_{3}\ldots\text{ with }x_{n}\neq 9\text{ for every }n,\\0,&\text{otherwise.}\end{cases}
\]

## Solution

Let \(A=\{x:f(x)=1\}\). The solutions PDF builds \(A\) by deleting decimals that use the digit \(9\): the \(n\)th step removes \(9^{n-1}\) intervals of length \(10^{-n}\). The removed measure is

\[
\frac1{10}\sum_{n=0}^{\infty}\left(\frac{9}{10}\right)^{n}=1,
\]

so \(A\) has Lebesgue measure \(0\). Therefore \(\int_{0}^{1}f(x)\,dx=0\).

## Final answer

\[
0.
\]

## SymPy self-check

SymPy sums \(\frac1{10}\sum_{n\ge 0}(9/10)^{n}\) to \(1\), which is the removed measure in the solutions PDF.
