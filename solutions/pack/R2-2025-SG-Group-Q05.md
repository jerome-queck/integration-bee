# R2-2025-SG-Group-Q05

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 5). The same integral is group 4 of `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK group 4)
- Worked source: derived in this note.
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
The UK mark scheme prints \(2-\pi^{2}/6\) for this integral.

## Final answer

\[
2-\dfrac{\pi^{2}}{6}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_group_q05`. SymPy checks the same slice integral and closed sum as the UK group 4 note.
