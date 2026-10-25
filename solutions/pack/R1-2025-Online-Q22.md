# R1-2025-Online-Q22

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 22)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 22)
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}\Biggl(\frac{x}{(2^{x}-1)^{2}}-\frac{4x}{(4^{x}-1)^{2}}\Biggr)\,dx.
\]

## Solution

The solutions PDF multiplies and divides by \(x\) and recognises a Frullani integrand. With \(f(t)=t^{2}/(2^{t}-1)^{2}\),
\[
\frac{x}{(2^{x}-1)^{2}}-\frac{4x}{(4^{x}-1)^{2}}=\frac{f(x)-f(2x)}{x}.
\]
The endpoint values are \(f(0+)=1/(\ln 2)^{2}\) and \(f(\infty)=0\), so the integral equals
\[
\frac{1}{(\ln 2)^{2}}\ln 2=\frac{1}{\ln 2}.
\]
The same PDF warns that separating the two summands is invalid: each integral diverges, and the substitution that seems to give \(0\) is not justified. The mark scheme prints \(1/\ln 2\).

## Final answer

\[
\dfrac{1}{\ln 2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q22`. SymPy checks the Frullani split, the limit \(f(0+)=1/(\ln 2)^{2}\), the limit \(f(\infty)=0\), and the product \((\ln 2)/(\ln 2)^{2}\).
