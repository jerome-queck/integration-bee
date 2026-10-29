# YANG-2.4-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 6, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^∞ √x e^{-√x} dx.

Catalog integrand `sqrt(x)*exp(-sqrt(x))`, limits `['0', 'oo']`, display `\sqrt{x} e^{- \sqrt{x}}`.

## Solution

Let \(u=\sqrt{x}\), so \(dx=2u\,du\). Then
\[
\int_0^\infty u e^{-u}\cdot 2u\,du=2\int_0^\infty u^2 e^{-u}\,du=2\cdot 2!=4.
\]

## Final answer

The catalog stores `answer_sympy` as `4` and `answer_latex` as `4`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
