# R1-2025-Online-Q08

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 8)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 8)
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}\Bigl(1-\frac{x}{1}\Bigl(1-\frac{x}{2}\Bigl(1-\frac{x}{3}\bigl(1-\cdots\bigr)\Bigr)\Bigr)\Bigr)\,dx.
\]

## Solution

The solutions PDF expands the nest. Truncating after \(n\) factors produces the partial sum of \(e^{-x}\):
\[
\sum_{k=0}^{n}\frac{(-x)^{k}}{k!}.
\]
The infinite nest is \(e^{-x}\), and \(\int_0^{\infty}e^{-x}\,dx=1\). The mark scheme prints \(1\).

## Final answer

\[
1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q08`. SymPy checks that the nest through \(n=6\) equals \(\sum_{k=0}^{6}(-x)^{k}/k!\) and evaluates \(\int_0^{\infty}e^{-t}\,dt=1\).
