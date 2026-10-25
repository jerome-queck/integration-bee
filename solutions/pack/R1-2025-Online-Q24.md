# R1-2025-Online-Q24

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 24)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 24)
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}\frac{x^{2}+\dfrac{2^{-x/6}}{7}-\dfrac{2^{-x/7}}{6}}{\bigl(2^{-x/7}+36x^{2}\bigr)\bigl(2^{-x/6}+49x^{2}\bigr)}\,dx.
\]

## Solution

The solutions PDF rewrites the integrand as
\[
\frac{1}{x}\Biggl(\frac{6x/42}{2^{-6x/42}+(6x)^{2}}-\frac{7x/42}{2^{-7x/42}+(7x)^{2}}\Biggr).
\]
That is \((f(6x)-f(7x))/x\) with
\[
f(t)=\frac{t/42}{2^{-t/42}+t^{2}}.
\]
The endpoint values are \(f(0+)=0\) and \(f(\infty)=0\), the second because \(t f(t)\to 1/42\). A Frullani integral with equal endpoint values is \(0\). The mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q24`. SymPy checks that the printed rational function equals \((f(6x)-f(7x))/x\), that \(f(0+)=0\), and that \(t f(t)\to 1/42\).
