# R2-2025-UK-Group-Q03

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (group 3)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (group 3)
- Worked source: derived in this note; the mark scheme prints the final value.
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

`solutions/self_check.py` runs `check_r2_2025_uk_group_q03`. SymPy checks the difference of squares and evaluates both quarter-disk integrals.
