# YANG-2.3-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 6, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ x (2x-1)^{1/3} dx.

Catalog integrand `x*(2*x - 1)**(1/3)`, limits `[]`, display `x \sqrt[3]{2 x - 1}`.

## Solution

Let \(u=2x-1\), so \(x=(u+1)/2\) and \(dx=du/2\). Then
\[
\frac14\int(u^{4/3}+u^{1/3})\,du=\frac{3}{28}u^{7/3}+\frac{3}{16}u^{4/3}.
\]
The gate stores the expanded real form in powers of \((2x-1)^{1/3}\). Differentiating that expression recovers \(x(2x-1)^{1/3}\).

## Final answer

The catalog stores `answer_sympy` as `3*x**2*(2*x - 1)**(1/3)/7 - 3*x*(2*x - 1)**(1/3)/56 - 9*(2*x - 1)**(1/3)/112` and `answer_latex` as `\frac{3 x^{2} \sqrt[3]{2 x - 1}}{7} - \frac{3 x \sqrt[3]{2 x - 1}}{56} - \frac{9 \sqrt[3]{2 x - 1}}{112}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
