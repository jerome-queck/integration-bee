# R2-2025-UK-Relay-Q12

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 12)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 12)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{-1}^{1}\frac{1+\operatorname{Li}_{2}(x)}{4+\operatorname{Li}_{2}(x^{2})}\,dx,
\]
where \(\operatorname{Li}_{2}(x)=-\int_{0}^{x}\ln(1-t)/t\,dt\).

## Solution

Differentiating the given definition produces \(\operatorname{Li}_{2}'(x)=-\ln(1-x)/x\). Therefore
\[
\frac{d}{dx}\bigl(\operatorname{Li}_{2}(x)+\operatorname{Li}_{2}(-x)\bigr)=-\frac{\ln(1-x^{2})}{x}=\frac12\frac{d}{dx}\operatorname{Li}_{2}(x^{2}),
\]
because \((1-x)(1+x)=1-x^{2}\) and both sides vanish at \(0\). Hence \(\operatorname{Li}_{2}(x)+\operatorname{Li}_{2}(-x)=\tfrac12\operatorname{Li}_{2}(x^{2})\). If \(f\) is the integrand and \(L=\operatorname{Li}_{2}(x^{2})\),
\[
f(x)+f(-x)=\frac{2+L/2}{4+L}=\frac12.
\]
The integral from \(-1\) to \(1\) is \(\int_{0}^{1}\tfrac12\,dx=1/2\). The mark scheme prints \(1/2\).

## Final answer

\[
\frac12.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q12`. SymPy checks \((1-x)(1+x)=1-x^{2}\) and \((2+L/2)/(4+L)=1/2\), then evaluates \(\int_{0}^{1}\tfrac12\,dx\).
