# YANG-2.3-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 1, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ e^{√x} dx.

Catalog integrand `exp(sqrt(x))`, limits `[]`, display `e^{\sqrt{x}}`.

## Solution

Let \(u=\sqrt{x}\), so \(x=u^2\) and \(dx=2u\,du\). The integral becomes
\[
\int 2u e^{u}\,du=2e^{u}(u-1)=2e^{\sqrt{x}}(\sqrt{x}-1).
\]
Differentiating the stored expression recovers \(e^{\sqrt{x}}\).

## Final answer

The catalog stores `answer_sympy` as `2*sqrt(x)*exp(sqrt(x)) - 2*exp(sqrt(x))` and `answer_latex` as `2 \sqrt{x} e^{\sqrt{x}} - 2 e^{\sqrt{x}}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
