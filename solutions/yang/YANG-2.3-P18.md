# YANG-2.3-P18

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 18, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ √(1-√x) dx.

Catalog integrand `sqrt(1 - sqrt(x))`, limits `[]`, display `\sqrt{1 - \sqrt{x}}`.

## Solution

Let \(u=\sqrt{x}\), so \(dx=2u\,du\). Then let \(t=1-u\):
\[
\int 2u\sqrt{1-u}\,du=-2\int(t^{1/2}-t^{3/2})\,dt=-\frac43 t^{3/2}+\frac45 t^{5/2}.
\]
The antiderivative is \(-\frac43(1-\sqrt{x})^{3/2}+\frac45(1-\sqrt{x})^{5/2}\). The gate stores the expanded equivalent in the factor \(\sqrt{1-\sqrt{x}}\). Differentiating that expression recovers the integrand.

## Final answer

The catalog stores `answer_sympy` as `-4*sqrt(x)*sqrt(1 - sqrt(x))/15 + 4*x*sqrt(1 - sqrt(x))/5 - 8*sqrt(1 - sqrt(x))/15` and `answer_latex` as `- \frac{4 \sqrt{x} \sqrt{1 - \sqrt{x}}}{15} + \frac{4 x \sqrt{1 - \sqrt{x}}}{5} - \frac{8 \sqrt{1 - \sqrt{x}}}{15}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
