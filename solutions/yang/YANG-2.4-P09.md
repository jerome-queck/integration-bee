# YANG-2.4-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 9, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_{-∞}^∞ e^{3x-e^x} dx.

Catalog integrand `exp(3*x - exp(x))`, limits `['-oo', 'oo']`, display `e^{3 x - e^{x}}`.

## Solution

Let \(u=e^x\), so \(dx=du/u\) and the limits run from \(0\) to \(\infty\). Then \(e^{3x-e^x}=u^3 e^{-u}\), and
\[
\int_0^\infty u^3 e^{-u}\frac{du}{u}=\int_0^\infty u^2 e^{-u}\,du=2!=2.
\]

## Final answer

The catalog stores `answer_sympy` as `2` and `answer_latex` as `2`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
