# R1-2025-Online-Q17

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 17)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 17)
- The catalog row is not changed.

## Problem

\[
\int_{1}^{\infty}\frac{1}{x+n x^{n}}\,dx,\qquad n>1.
\]

## Solution

Divide the numerator and the denominator by \(x^{n}\), as in the solutions PDF:
\[
\int_{1}^{\infty}\frac{dx}{x+nx^{n}}=\int_{1}^{\infty}\frac{x^{-n}}{x^{1-n}+n}\,dx.
\]
The antiderivative is \(\ln(x^{1-n}+n)/(1-n)\). For \(n>1\) the power \(x^{1-n}\) vanishes at infinity, so the definite integral is
\[
\frac{\ln n}{1-n}-\frac{\ln(n+1)}{1-n}=\frac{1}{1-n}\ln\frac{n}{n+1}.
\]
The condition \(n>1\) is what the solutions PDF uses for convergence. The mark scheme prints \(\dfrac{1}{1-n}\ln\dfrac{n}{n+1}\).

## Final answer

\[
\dfrac{1}{1-n}\ln\dfrac{n}{n+1}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q17`. SymPy differentiates \(\ln(x^{1-n}+n)/(1-n)\) and checks that the endpoint difference is \(\ln(n/(n+1))/(1-n)\).
