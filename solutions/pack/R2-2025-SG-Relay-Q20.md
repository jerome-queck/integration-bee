# R2-2025-SG-Relay-Q20

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (PDF page 6, relay 20). The same integral is relay 12 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (PDF page 3, UK relay 12)
- Worked source: derived in this note; the UK mark scheme prints the final value.

## Problem

\[
\int_{-1}^{1}\frac{1+\operatorname{Li}_{2}(x)}{4+\operatorname{Li}_{2}(x^{2})}\,dx,
\]

where \(\operatorname{Li}_{2}(x)=-\int_{0}^{x}\log(1-t)/t\,dt\).

## Solution

Let \(L(x)=\operatorname{Li}_{2}(x^{2})\). The derivative of \(\operatorname{Li}_{2}(x)+\operatorname{Li}_{2}(-x)-L(x)/2\) is

\[
\frac{-\log(1-x)-\log(1+x)+\log(1-x^{2})}{x}=0
\]

on \((-1,1)\), and the function vanishes at \(0\). Thus \(\operatorname{Li}_{2}(x)+\operatorname{Li}_{2}(-x)=L(x)/2\). If \(f\) is the integrand, then

\[
f(x)+f(-x)=\frac{2+L(x)/2}{4+L(x)}=\frac12.
\]

On \([0,1]\), \(\operatorname{Li}_{2}\) increases from \(0\) to \(\operatorname{Li}_{2}(1)=\pi^{2}/6\), so the denominator is at least \(4\). Therefore

\[
\int_{-1}^{1}f(x)\,dx=\int_{0}^{1}\frac12\,dx=\frac12.
\]

The UK mark scheme prints \(1/2\).

## Final answer

\[
\frac{1}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q20`. SymPy checks \(\operatorname{Li}_{1}(z)=-\log(1-z)\), the cancellation of the logarithmic derivative, the value at \(0\), and the rational average \((2+L/2)/(4+L)=1/2\).

The pack gate verifies the logarithm identity on the positive parameterization \(x=u/(1+u)\), checks the constant at zero and positivity of the denominator, then integrates the exact reflected sum.
