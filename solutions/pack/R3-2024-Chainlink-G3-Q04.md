# R3-2024-Chainlink-G3-Q04

- Problem: `sources/past/r3/2024/Chainlink_Game_3_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 4)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 3, problem 4)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 3, problem 4)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/4}\frac{\sin(2x)}{\sin x+\cos x+1}\,dx.
\]

## Solution

Let \(a=\sin x+\cos x\). Then \(a^{2}-1=\sin(2x)\), and

\[
\frac{a^{2}-1}{a+1}=a-1=\sin x+\cos x-1.
\]

Integrating from \(0\) to \(\pi/4\) gives

\[
\bigl[\sin x-\cos x-x\bigr]_{0}^{\pi/4}=1-\frac{\pi}{4}.
\]

## Final answer

\[
1-\dfrac{\pi}{4}.
\]

## SymPy self-check

SymPy checks \((\sin x+\cos x)^{2}-1=\sin(2x)\) and \(((a^{2}-1)/(a+1))=a-1\). It evaluates \(\int_{0}^{\pi/4}(\sin x+\cos x-1)\,dx=1-\pi/4\).
