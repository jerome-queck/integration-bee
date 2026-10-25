# R1-2025-Online-Q23

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 23)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 23)
- The catalog row is not changed.

## Problem

\[
\int_1^{e}\Biggl(\sqrt{\ln x}+\frac{1}{e-1}\exp\Biggl(\Biggl(\frac{x-1}{e-1}\Biggr)^{2}\Biggr)\Biggr)\,dx.
\]

## Solution

The solutions PDF splits the integrand. The second piece, with \(y=(x-1)/(e-1)\), is \(\int_0^1 e^{y^{2}}\,dy\). The functions \(\sqrt{\ln x}\) on \([1,e]\) and \(\exp(y^{2})\) on \([0,1]\) are inverses. The inverse-function identity
\[
\int_1^{e}\sqrt{\ln x}\,dx+\int_0^1 e^{y^{2}}\,dy=e\cdot 1-1\cdot 0=e
\]
is the whole integral. The mark scheme prints \(e\).

## Final answer

\[
e.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q23`. SymPy checks that \(\exp((\sqrt{\ln x})^{2})=x\), that the derivative of \(b\sqrt{\ln b}\) carries the inverse boundary term, and that the endpoint combination is \(e\).
