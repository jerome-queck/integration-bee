# R2-2025-UK-Group-Q09

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (group 9)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (group 9)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\sum_{n=1}^{\infty}\int_{0}^{1}(-1)^{n}\ln\Bigl(\frac{1-x^{1/n}}{1-x^{1/(n+1)}}\Bigr)\,dx.
\]

## Solution

The beta function \(B(n,s)=\Gamma(n)\Gamma(s)/\Gamma(n+s)\) satisfies \(B(n,1)=1/n\), and
\[
\frac{\partial B}{\partial s}=B\bigl(\psi(s)-\psi(n+s)\bigr).
\]
At \(s=1\) this derivative is \(-H_{n}/n\), because \(\psi(n+1)+\gamma=H_{n}\). The substitution \(x=v^{n}\) therefore gives
\[
\int_{0}^{1}\ln(1-x^{1/n})\,dx=-H_{n}.
\]
The difference of the two logarithms integrates to \(H_{n+1}-H_{n}=1/(n+1)\). The series is
\[
\sum_{n\ge 1}\frac{(-1)^{n}}{n+1}=\ln 2-1.
\]
The mark scheme prints \(\ln 2-1\).

## Final answer

\[
\ln 2-1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_group_q09`. SymPy checks the beta derivative, the digamma form of \(H_{n}\), and the alternating harmonic tail.
