# YANG-2.3-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 9, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ ln(x)^3 dx.

Catalog integrand `log(x)**3`, limits `[]`, display `\log{\left(x \right)}^{3}`.

## Solution

Three integrations by parts, each time differentiating a power of \(\ln x\) and integrating \(1\), give
\[
x\ln^3 x-3x\ln^2 x+6x\ln x-6x.
\]
Differentiating that polynomial in \(\ln x\) recovers \(\ln^3 x\).

## Final answer

The catalog stores `answer_sympy` as `x*log(x)**3 - 3*x*log(x)**2 + 6*x*log(x) - 6*x` and `answer_latex` as `x \log{\left(x \right)}^{3} - 3 x \log{\left(x \right)}^{2} + 6 x \log{\left(x \right)} - 6 x`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
