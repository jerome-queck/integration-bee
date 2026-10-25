# R2-2025-UK-Relay-Q13

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 13)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 13)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{-\infty}^{\infty}e^{x-\sinh^{2}x}\,dx.
\]

## Solution

Set \(s=e^{x}\), so \(dx=ds/s\) and \(s\) runs over \((0,\infty)\). Then \(e^{x}/s=1\) and
\[
e^{-\sinh^{2}(\ln s)}=\sqrt{e}\,\exp\Bigl(-\frac{s^{2}}{4}-\frac{1}{4s^{2}}\Bigr).
\]
The integral is
\[
\sqrt{e}\int_{0}^{\infty}\exp\Bigl(-\frac{s^{2}}{4}-\frac{1}{4s^{2}}\Bigr)\,ds=\sqrt{\pi}.
\]
The mark scheme prints \(\sqrt{\pi}\).

## Final answer

\[
\sqrt{\pi}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q13`. SymPy checks the exponential substitution and evaluates the resulting Gaussian integral.
