# R2-2025-UK-Group-Q04

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (group 4)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (group 4)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{1}^{\infty}\{x\}\,\Bigl\lfloor\frac{2}{\{x\}}\Bigr\rfloor^{-\lfloor x\rfloor}\,dx.
\]

## Solution

Write \(x=n+f\) with \(n\ge 1\) and \(f\in(0,1)\). Then \(\lfloor 2/f\rfloor=k\) for \(f\in(2/(k+1),2/k]\) and \(k\ge 2\). The piece is
\[
k^{-n}\int_{2/(k+1)}^{2/k}f\,df=2k^{-n}\Bigl(\frac{1}{k^{2}}-\frac{1}{(k+1)^{2}}\Bigr).
\]
Summing \(n\ge 1\) uses \(\sum_{n\ge 1}k^{-n}=1/(k-1)\), so the integral is
\[
2\sum_{k\ge 2}\frac{1}{k-1}\Bigl(\frac{1}{k^{2}}-\frac{1}{(k+1)^{2}}\Bigr)=2-\frac{\pi^{2}}{6}.
\]
The mark scheme prints \(2-\pi^{2}/6\). The stored catalog answer for this row is a different relay value; the mark-scheme line for group 4 is the one used here.

## Final answer

\[
2-\dfrac{\pi^{2}}{6}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_group_q04`. SymPy checks the slice integral, the geometric sum \(1/(k-1)\), and the closed double sum.
