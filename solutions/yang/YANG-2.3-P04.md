# YANG-2.3-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 4, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ dx/√(√x+1).

Catalog integrand `1/sqrt(sqrt(x) + 1)`, limits `[]`, display `\frac{1}{\sqrt{\sqrt{x} + 1}}`.

## Solution

Let \(u=\sqrt{x}\), so \(dx=2u\,du\). Then let \(t=u+1\):
\[
\int\frac{2u}{\sqrt{u+1}}\,du=2\int\bigl(t^{1/2}-t^{-1/2}\bigr)\,dt=\frac43 t^{3/2}-4t^{1/2}.
\]
Back-substituting gives \(\frac43(\sqrt{x}+1)^{3/2}-4\sqrt{\sqrt{x}+1}\). The gate stores the expanded equivalent
\(\frac43\sqrt{x}\,\sqrt{\sqrt{x}+1}-\frac83\sqrt{\sqrt{x}+1}\). Differentiating that expression recovers the integrand.

## Final answer

The catalog stores `answer_sympy` as `4*sqrt(x)*sqrt(sqrt(x) + 1)/3 - 8*sqrt(sqrt(x) + 1)/3` and `answer_latex` as `\frac{4 \sqrt{x} \sqrt{\sqrt{x} + 1}}{3} - \frac{8 \sqrt{\sqrt{x} + 1}}{3}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
