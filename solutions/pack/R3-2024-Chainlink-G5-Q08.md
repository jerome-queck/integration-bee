# R3-2024-Chainlink-G5-Q08

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 8)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 8)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 8)
- The catalog row is not changed.

## Problem

\[
\int\frac{\cos x+1-x^{2}}{(x\sin x+1)\sqrt{1-x^{2}}}\,dx.
\]

## Solution

Set

\[
y=\frac{x+\sin x}{x\sin x+1}.
\]

The solutions PDF computes

\[
y'=\frac{(\cos x+1-x^{2})\cos x}{(x\sin x+1)^{2}}.
\]

Comparing this with the integrand leaves the factor

\[
\frac{x\sin x+1}{\sqrt{(1-\sin^{2}x)(1-x^{2})}}=\frac{1}{\sqrt{1-y^{2}}}.
\]

The integral is therefore \(\int dy/\sqrt{1-y^{2}}=\arcsin y+C\).

## Final answer

\[
\arcsin\left(\dfrac{x+\sin x}{x\sin x+1}\right)+C.
\]

## SymPy self-check

SymPy checks the displayed formula for \(y'\). It also checks \((x\sin x+1)^{2}(1-y^{2})=(1-\sin^{2}x)(1-x^{2})\), which is the squared form of the remaining factor.
