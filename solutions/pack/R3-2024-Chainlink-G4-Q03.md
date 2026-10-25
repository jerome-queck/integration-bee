# R3-2024-Chainlink-G4-Q03

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 3)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 3)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 3)
- The catalog row is not changed.

## Problem

\[
\int_{1}^{\infty}\frac{(-1)^{\lceil x\rceil}}{\sqrt{\lfloor x\rfloor\lceil x\rceil}\bigl(\sqrt{\lceil x\rceil}-\sqrt{\lfloor x\rfloor}\bigr)}\,dx.
\]

## Solution

On \((n,n+1)\) the floor is \(n\) and the ceiling is \(n+1\). Rationalising \(\sqrt{n+1}-\sqrt{n}\) produces

\[
\sum_{n=1}^{\infty}(-1)^{n+1}\left(\frac{1}{\sqrt{n}}+\frac{1}{\sqrt{n+1}}\right).
\]

Pairing \(n=2k-1\) with \(n=2k\) leaves the telescoping difference \(1/\sqrt{2k-1}-1/\sqrt{2k+1}\). The partial sum through \(k=m\) is \(1-1/\sqrt{2m+1}\), and the series sums to \(1\).

## Final answer

\[
1.
\]

## SymPy self-check

SymPy simplifies the paired summand to \(1/\sqrt{2k-1}-1/\sqrt{2k+1}\) and sums the first \(m\) pairs to \(1-1/\sqrt{2m+1}\).
