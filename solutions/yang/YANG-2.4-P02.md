# YANG-2.4-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 2, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^1 ln(x)^6 dx.

Catalog integrand `log(x)**6`, limits `['0', '1']`, display `\log{\left(x \right)}^{6}`.

## Solution

Let \(u=-\ln x\), so \(x=e^{-u}\) and \(dx=e^{-u}\,du\). The limits \(x\to 0^+\) and \(x=1\) become \(u\to\infty\) and \(u=0\), and \((\ln x)^6=u^6\). Therefore
\[
\int_0^1\ln^6 x\,dx=\int_0^\infty u^6 e^{-u}\,du=6!=720.
\]

## Final answer

The catalog stores `answer_sympy` as `720` and `answer_latex` as `720`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
