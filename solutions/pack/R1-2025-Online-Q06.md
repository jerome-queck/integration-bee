# R1-2025-Online-Q06

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 6)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 6)
- The catalog row is not changed.

## Problem

\[
\int_0^1\sqrt{-\ln x}\,dx.
\]

## Solution

Set \(u=-\ln x\). Then \(dx=e^{-u}\,du\), and the limits change from \(x=1\) to \(x=0\) into \(u=0\) to \(u=\infty\):
\[
\int_0^\infty\sqrt{u}\,e^{-u}\,du=\Gamma\Bigl(\frac32\Bigr)=\frac12\Gamma\Bigl(\frac12\Bigr)=\frac{\sqrt\pi}{2}.
\]
The mark scheme prints \(\sqrt{\pi}/2\).

## Final answer

\[
\frac{\sqrt\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q06`. SymPy evaluates \(\int_0^\infty\sqrt{s}\,e^{-s}\,ds=\sqrt{\pi}/2\).
