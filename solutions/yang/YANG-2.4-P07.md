# YANG-2.4-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 7, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^∞ e^{-x^{1/3}} x^{-1/3} dx.

Catalog integrand `exp(-x**(1/3))/x**(1/3)`, limits `['0', 'oo']`, display `\frac{e^{- \sqrt[3]{x}}}{\sqrt[3]{x}}`.

## Solution

Let \(u=x^{1/3}\), so \(x=u^3\) and \(dx=3u^2\,du\). The integrand becomes
\[
e^{-u}u^{-1}\cdot 3u^2\,du=3u e^{-u}\,du,
\]
and \(\int_0^\infty 3u e^{-u}\,du=3\cdot 1!=3\).

## Final answer

The catalog stores `answer_sympy` as `3` and `answer_latex` as `3`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
