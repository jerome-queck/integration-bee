# YANG-2.4-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 3, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_{-∞}^0 e^x (x^4+x^3+x^2+x) dx.

Catalog integrand `(x**4 + x**3 + x**2 + x)*exp(x)`, limits `['-oo', '0']`, display `\left(x^{4} + x^{3} + x^{2} + x\right) e^{x}`.

## Solution

Let \(u=-x\). The limits \(x\to-\infty\) and \(x=0\) become \(u\to\infty\) and \(u=0\), and
\[
\int_0^\infty e^{-u}(u^4-u^3+u^2-u)\,du=4!-3!+2!-1!=24-6+2-1=19.
\]

## Final answer

The catalog stores `answer_sympy` as `19` and `answer_latex` as `19`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
