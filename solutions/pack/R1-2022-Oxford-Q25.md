# R1-2022-Oxford-Q25

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 25)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi/2}(\ln\tan\theta)^{2}\,d\theta.
\]

## Solution

The Fourier series \(\ln(\sin\theta)=-\ln 2-\sum_{k\ge 1}\cos(2k\theta)/k\) gives
\[
\ln(\tan\theta)=-2\sum_{m\ge 0}\frac{\cos\bigl(2(2m+1)\theta\bigr)}{2m+1}
\]
on \((0,\pi/2)\). The cosines are orthogonal there, and \(\int_0^{\pi/2}\cos^{2}(2(2m+1)\theta)\,d\theta=\pi/4\), so
\[
\int_0^{\pi/2}(\ln\tan\theta)^{2}\,d\theta=\pi\sum_{m\ge 0}\frac{1}{(2m+1)^{2}}=\pi\cdot\frac{\pi^{2}}{8}=\frac{\pi^{3}}{8}.
\]
The mark scheme prints \(\pi^{3}/8\).

## Final answer

\[
\dfrac{\pi^{3}}{8}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q25`. A quadrature of \((\ln\tan\theta)^{2}\) on \((0,\pi/2)\) matches \(\pi^{3}/8\) to within \(10^{-8}\).
