# R1-2022-Oxford-Q20

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 20)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}\frac{x^{2}}{e^{x}-1}\,dx.
\]

## Solution

For \(x>0\),
\[
\frac{1}{e^{x}-1}=\sum_{k\ge 1}e^{-kx}.
\]
Each term integrates by parts, or by the gamma integral, to
\[
\int_0^{\infty}x^{2}e^{-kx}\,dx=\frac{2}{k^{3}}.
\]
The sum is \(2\zeta(3)\). The mark scheme prints \(2\zeta(3)\).

## Final answer

\[
2\zeta(3).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q20`. SymPy evaluates \(\int_0^{\infty}x^{2}e^{-kx}\,dx=2/k^{3}\) and sums that series to \(2\zeta(3)\).
