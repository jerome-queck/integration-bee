# YANG-2.4-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 5, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^∞ e^{-x} (x+1)^4 dx.

Catalog integrand `(x + 1)**4*exp(-x)`, limits `['0', 'oo']`, display `\left(x + 1\right)^{4} e^{- x}`.

## Solution

Let \(u=x+1\). The integral becomes
\[
e\int_1^\infty u^4 e^{-u}\,du.
\]
For a positive integer power, \(\int_1^\infty u^4 e^{-u}\,du=4!\,e^{-1}\sum_{k=0}^{4}1/k!\). The sum is \(1+1+1/2+1/6+1/24=65/24\), so the factor \(e\cdot 24\cdot e^{-1}\cdot 65/24\) equals \(65\).

## Final answer

The catalog stores `answer_sympy` as `65` and `answer_latex` as `65`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
