# R2-2025-SG-Group-Q08

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 8). The same integral is group 7 of `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK group 7)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{-\infty}^{\infty}\frac{dx}{(e+e^{x})(x^{4}-4x^{3}+6x^{2}-4x+2)}.
\]

## Solution

The quartic is \((x-1)^{4}+1\). Set \(t=x-1\). Then \(e+e^{x}=e(1+e^{t})\), and the integral is
\[
\frac{1}{e}\int_{-\infty}^{\infty}\frac{dt}{(1+e^{t})(t^{4}+1)}.
\]
The sum of the integrand with its reflection is \(1/(t^{4}+1)\), so the integral is half of \(\int_{-\infty}^{\infty}dt/(t^{4}+1)=\pi/\sqrt{2}\). The value is \(\pi/(2e\sqrt{2})\). The mark scheme prints \(\pi/(2e\sqrt{2})\).

## Final answer

\[
\dfrac{\pi}{2e\sqrt{2}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_group_q08`. SymPy checks the same reflection identity as the UK group 7 note.
