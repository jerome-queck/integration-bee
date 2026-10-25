# R3-2024-Chainlink-G5-Q07

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 7)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 7)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 7)
- The catalog row is not changed.

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

SymPy checks \(\arctan\sqrt{3}=\pi/3\) and the printed sector formula \(\pi/12\). Splitting one period at the intersection \(x=1/4\), the integral of the semicircle on \([0,1/4]\) plus the integral of the line on \([1/4,1/2]\), doubled, is also \(\pi/12\).
