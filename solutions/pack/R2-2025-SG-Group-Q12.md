# R2-2025-SG-Group-Q12

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 12). The same series of integrals is group 9 of `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK group 9)
- Worked source: derived in this note.
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

`solutions/self_check.py` runs `check_r2_2025_sg_group_q12`. SymPy checks the same beta derivative and alternating harmonic tail as the UK group 9 note.
