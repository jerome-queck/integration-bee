# R3-2024-Chainlink-G3-Q07

- Problem: `sources/past/r3/2024/Chainlink_Game_3_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 7)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 3, problem 7)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 3, problem 7)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{2}(3x^{2}-5x+3)\cos(x^{3}-3x^{2}+4x-2)\,dx.
\]

## Solution

The shift \(x=u+1\) moves the interval to \([-1,1]\) and the integrand to \((3u^{2}+u+1)\cos(u^{3}+u)\). The summand \(u\cos(u^{3}+u)\) is odd, so it integrates to \(0\). The even summand is a derivative:

\[
\int_{-1}^{1}(3u^{2}+1)\cos(u^{3}+u)\,du=\bigl[\sin(u^{3}+u)\bigr]_{-1}^{1}=2\sin 2.
\]

## Final answer

\[
2\sin 2.
\]

## SymPy self-check

SymPy expands the shifted coefficient to \(3u^{2}+u+1\) and the phase to \(u^{3}+u\). It checks that \(u\cos(u^{3}+u)\) is odd, differentiates \(\sin(u^{3}+u)\) to \((3u^{2}+1)\cos(u^{3}+u)\), and evaluates the endpoints as \(2\sin 2\).
