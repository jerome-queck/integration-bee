# R3-2024-Chainlink-G2-Q04

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 4)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 4)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 4)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\ln(1+e^{-x})\cos x\,dx.
\]

## Solution

The solutions PDF expands \(\ln(1+e^{-x})=\sum_{k\ge 1}(-1)^{k-1}e^{-kx}/k\) and integrates term by term:

\[
\int_{0}^{\infty}e^{-kx}\cos x\,dx=\frac{k}{k^{2}+1}.
\]

The series that remains is \(\sum_{k\ge 1}(-1)^{k-1}/(k^{2}+1)\), which the solutions PDF evaluates as \(\frac12-\frac{\pi}{2}\operatorname{csch}\pi\).

## Final answer

\[
\dfrac{1}{2}-\dfrac{\pi}{2}\operatorname{csch}\pi.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{\infty}e^{-kx}\cos x\,dx=k/(k^{2}+1)\) for \(k>0\). The alternating partial sum through \(k=800\) lies within one omitted term of \(\frac12-(\pi/2)\operatorname{csch}\pi\).
