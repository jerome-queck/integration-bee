# YANG-2.3-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 13, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ dx/(∛(x+1)-1).

Catalog integrand `1/((x + 1)**(1/3) - 1)`, limits `[]`, display `\frac{1}{\sqrt[3]{x + 1} - 1}`.

## Solution

Let \(u=\sqrt[3]{x+1}\), so \(dx=3u^2\,du\). Polynomial division gives \(u^2/(u-1)=u+1+1/(u-1)\), and
\[
3\int\Bigl(u+1+\frac{1}{u-1}\Bigr)\,du=\frac32 u^2+3u+3\ln|u-1|.
\]
On each interval where \(u>1\) or \(u<1\), the logarithm without the absolute value has the same derivative. The stored antiderivative is
\(\frac32(x+1)^{2/3}+3(x+1)^{1/3}+3\ln\bigl((x+1)^{1/3}-1\bigr)\).

## Final answer

The catalog stores `answer_sympy` as `3*(x + 1)**(2/3)/2 + 3*(x + 1)**(1/3) + 3*log((x + 1)**(1/3) - 1)` and `answer_latex` as `\frac{3 \left(x + 1\right)^{\frac{2}{3}}}{2} + 3 \sqrt[3]{x + 1} + 3 \log{\left(\sqrt[3]{x + 1} - 1 \right)}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
