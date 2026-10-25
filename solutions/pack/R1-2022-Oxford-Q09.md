# R1-2022-Oxford-Q09

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 9)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{2\pi}\sin(\sin x-x)\,dx.
\]

## Solution

Let \(f(x)=\sin(\sin x-x)\). The substitutions \(x=\pi+t\) and \(x=\pi-t\) give
\[
f(\pi+t)=\sin(t+\sin t),\qquad f(\pi-t)=-\sin(t+\sin t),
\]
so \(f(\pi+t)+f(\pi-t)=0\). Pairing those points over a full period cancels the integral. The mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q09`. SymPy simplifies \(f(\pi+t)+f(\pi-t)\) to \(0\).
