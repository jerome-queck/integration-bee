# YANG-2.4-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 4, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^∞ x^5 e^{-x^2} dx.

Catalog integrand `x**5*exp(-x**2)`, limits `['0', 'oo']`, display `x^{5} e^{- x^{2}}`.

## Solution

Let \(u=x^2\), so \(x\,dx=du/2\) and \(x^4=u^2\). Then
\[
\int_0^\infty x^5 e^{-x^2}\,dx=\frac12\int_0^\infty u^2 e^{-u}\,du=\frac12\cdot 2!=1.
\]

## Final answer

The catalog stores `answer_sympy` as `1` and `answer_latex` as `1`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
