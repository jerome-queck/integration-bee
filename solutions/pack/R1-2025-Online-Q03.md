# R1-2025-Online-Q03

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 3)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 3)
- The catalog row is not changed.

## Problem

\[
\int_0^\infty\operatorname{sech}(2\ln x)\,dx.
\]

## Solution

The exponential form of the hyperbolic secant is
\[
\operatorname{sech}(2\ln x)=\frac{2}{x^2+x^{-2}}=\frac{2}{(x-x^{-1})^2+2}.
\]
The solutions PDF applies Glasser's master theorem, replacing \(x-1/x\) by \(x\), and the integral becomes
\[
\int_0^\infty\frac{2}{x^2+2}\,dx=\frac{\pi}{\sqrt{2}}.
\]
The mark scheme prints \(\pi/\sqrt{2}\).

## Final answer

\[
\frac{\pi}{\sqrt{2}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q03`. SymPy rewrites \(\operatorname{sech}(2\ln x)\) as \(2x^2/(x^4+1)\) and checks \(x^2+x^{-2}=(x-1/x)^2+2\). It evaluates \(\int_0^\infty 2/(x^2+2)\,dx\), and a quadrature of the original integrand matches \(\pi/\sqrt{2}\).
