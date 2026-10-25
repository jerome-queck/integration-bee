# R2-2025-SG-Group-Q04

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 4). The same integral is group 3 of `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK group 3)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{2x-1}{\sqrt{2x-x^{2}}-\sqrt{1-x^{2}}}\,dx.
\]

## Solution

The difference of squares in the denominator is
\[
(2x-x^{2})-(1-x^{2})=2x-1.
\]
Wherever the denominator is nonzero,
\[
\frac{2x-1}{\sqrt{2x-x^{2}}-\sqrt{1-x^{2}}}=\sqrt{2x-x^{2}}+\sqrt{1-x^{2}}.
\]
The identity extends by continuity through \(x=1/2\). Now \(2x-x^{2}=1-(x-1)^{2}\), so
\[
\int_{0}^{1}\sqrt{1-(x-1)^{2}}\,dx=\int_{-1}^{0}\sqrt{1-y^{2}}\,dy=\frac{\pi}{4}
\]
is a quarter disk, and \(\int_{0}^{1}\sqrt{1-x^{2}}\,dx=\pi/4\) is the other quarter. The sum is \(\pi/2\). The mark scheme prints \(\pi/2\).

## Final answer

\[
\frac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_group_q04`. SymPy checks the same difference of squares and quarter-disk integrals as the UK group 3 note.
