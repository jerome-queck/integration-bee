# R1-2025-Online-Q11

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 11)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 11)
- The catalog row is not changed.

## Problem

\[
\int\frac{1}{x\arcsin(\ln x)\sqrt{1-(\ln x)^{2}}}\,dx.
\]

## Solution

The solutions PDF rewrites the integrand so the chain rule is visible:
\[
\frac{1}{x\arcsin(\ln x)\sqrt{1-(\ln x)^{2}}}=\frac{1}{\arcsin(\ln x)}\cdot\frac{1}{x\sqrt{1-(\ln x)^{2}}}.
\]
The second factor is the derivative of \(\arcsin(\ln x)\). The antiderivative is \(\ln|\arcsin(\ln x)|+C\). The mark scheme prints the same expression.

## Final answer

\[
\ln|\arcsin(\ln x)|+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q11`. SymPy differentiates \(\ln(\arcsin(\ln x))\) back to the integrand for \(x>0\).
