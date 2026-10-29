# YANG-2.4-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 11, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^∞ x^{-7} e^{-1/x} dx.

Catalog integrand `exp(-1/x)/x**7`, limits `['0', 'oo']`, display `\frac{e^{- \frac{1}{x}}}{x^{7}}`.

## Solution

Let \(u=1/x\), so \(dx=-du/u^2\). The limits reverse from \(\infty\) to \(0\), and
\[
\int_\infty^0 u^{7} e^{-u}\Bigl(-\frac{du}{u^2}\Bigr)=\int_0^\infty u^5 e^{-u}\,du=5!=120.
\]

## Final answer

The catalog stores `answer_sympy` as `120` and `answer_latex` as `120`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
