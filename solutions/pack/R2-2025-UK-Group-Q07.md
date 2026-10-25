# R2-2025-UK-Group-Q07

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (group 7)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (group 7)
- Worked source: derived in this note; the mark scheme prints the final value.
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

`solutions/self_check.py` runs `check_r2_2025_uk_group_q07`. SymPy checks the quartic factorisation, the reflection identity, and \(\int dt/(t^{4}+1)\).
