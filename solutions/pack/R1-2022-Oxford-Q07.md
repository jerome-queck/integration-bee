# R1-2022-Oxford-Q07

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 7)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}e^{-x}\sqrt{1-e^{-2x}}\,dx.
\]

## Solution

Set \(u=e^{-x}\). Then \(du=-e^{-x}\,dx\), and the limits run from \(1\) to \(0\), so the integral is the quarter-circle area
\[
\int_0^1\sqrt{1-u^{2}}\,du=\frac{\pi}{4}.
\]
The mark scheme prints \(\pi/4\).

## Final answer

\[
\dfrac{\pi}{4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q07`. SymPy evaluates \(\int_0^1\sqrt{1-u^{2}}\,du=\pi/4\).
