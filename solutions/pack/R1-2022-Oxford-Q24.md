# R1-2022-Oxford-Q24

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 24)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1\ln x\cdot\sin(\ln x)\,dx.
\]

## Solution

Set \(x=e^{-u}\). Then \(\ln x=-u\) and the integral becomes
\[
\int_0^{\infty}ue^{-u}\sin u\,du=\frac12.
\]
The mark scheme prints \(1/2\).

## Final answer

\[
\dfrac12.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q24`. SymPy evaluates \(\int_0^{\infty}ue^{-u}\sin u\,du=1/2\).
