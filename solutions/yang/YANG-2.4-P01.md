# YANG-2.4-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 1, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^∞ x^5 e^{-x} dx.

Catalog integrand `x**5*exp(-x)`, limits `['0', 'oo']`, display `x^{5} e^{- x}`.

## Solution

The printed factorial integral is \(n!=\int_0^\infty x^n e^{-x}\,dx\). For \(n=5\),
\[
\int_0^\infty x^5 e^{-x}\,dx=5!=120.
\]
SymPy's exact evaluator returns \(120\).

## Final answer

The catalog stores `answer_sympy` as `120` and `answer_latex` as `120`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
