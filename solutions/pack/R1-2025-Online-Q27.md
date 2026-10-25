# R1-2025-Online-Q27

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 27)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 27)
- The catalog row is not changed.

## Problem

\[
\int\frac{2^{x}}{(1+\sqrt{3})^{x}+(2+\sqrt{3})^{x}}\,dx.
\]

## Solution

The solutions PDF factors \(2^{x}\) from the denominator. With \(r=(1+\sqrt{3})/2\), one has \(r^{2}=(2+\sqrt{3})/2\), so the integral is
\[
\frac{1}{\ln r}\int\frac{du}{u^{2}(u+1)},\qquad u=r^{x}.
\]
Partial fractions give \(-1/u+1/u^{2}+1/(u+1)\), whose antiderivative is \(\ln(1+1/u)-1/u\). Returning to \(x\) uses \(1/r=\sqrt{3}-1\) and \(\ln r=-\ln(\sqrt{3}-1)\). The mark scheme prints
\[
\frac{(\sqrt{3}-1)^{x}-\ln\bigl(1+(\sqrt{3}-1)^{x}\bigr)}{\ln(\sqrt{3}-1)}+C.
\]

## Final answer

\[
\dfrac{(\sqrt{3}-1)^{x}-\ln\bigl(1+(\sqrt{3}-1)^{x}\bigr)}{\ln(\sqrt{3}-1)}+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q27`. SymPy checks the partial fractions, \(r^{2}=(2+\sqrt{3})/2\), \(1/r=\sqrt{3}-1\), and \(\ln r+\ln(\sqrt{3}-1)=0\).
