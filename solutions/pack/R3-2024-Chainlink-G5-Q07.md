# R3-2024-Chainlink-G5-Q07

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 7)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 7)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 7)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[
\int_{0}^{2025}\min\left(\sqrt{\{x\}-\{x\}^{2}},\left|\frac{\sqrt{3}\arcsin(\cos(\pi x))}{\pi}\right|\right)\,dx.
\]

## Solution

On each unit interval the first expression is the upper semicircle of radius \(1/2\) centred at a half-integer. The absolute inverse sine is a piecewise-linear spike of height \(\sqrt{3}/2\) at the integers. The solutions PDF reads the area between consecutive integers as two sectors of the circle of radius \(1/2\), each of angle

\[
\arctan\left(\frac{\sqrt{3}/2}{1/2}\right)=\frac{\pi}{3}.
\]

Two such sectors have area

\[
2\cdot\frac{\pi/3}{2\pi}\cdot\frac{\pi}{4}=\frac{\pi}{12}.
\]

There are \(2025\) unit intervals, so the integral is \(2025\pi/12\).

## Final answer

\[
\dfrac{2025\pi}{12}.
\]

## SymPy self-check

The gate checks the period, the principal arcsine branch on one period, and the exact crossings at 1/4 and 3/4. It integrates the semicircle and line pieces symbolically, then multiplies by 2025.
