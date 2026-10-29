# YANG-2.3-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 5, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ (arcsin x)^2 dx.

Catalog integrand `asin(x)**2`, limits `[]`, display `\operatorname{asin}^{2}{\left(x \right)}`.

## Solution

Integrate by parts with \(v=(\arcsin x)^2\) and \(dw=dx\). The remaining integral is
\[
\int\frac{2x\arcsin x}{\sqrt{1-x^2}}\,dx.
\]
The substitution \(x=\sin\theta\) turns it into \(\int 2\theta\sin\theta\,d\theta=-2\theta\cos\theta+2\sin\theta\). Returning to \(x\) produces
\[
x(\arcsin x)^2+2\sqrt{1-x^2}\arcsin x-2x.
\]

## Final answer

The catalog stores `answer_sympy` as `x*asin(x)**2 - 2*x + 2*sqrt(1 - x**2)*asin(x)` and `answer_latex` as `x \operatorname{asin}^{2}{\left(x \right)} - 2 x + 2 \sqrt{1 - x^{2}} \operatorname{asin}{\left(x \right)}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
