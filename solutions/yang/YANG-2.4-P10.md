# YANG-2.4-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 10, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_1^∞ (ln(x)/x)^4 dx.

Catalog integrand `log(x)**4/x**4`, limits `['1', 'oo']`, display `\frac{\log{\left(x \right)}^{4}}{x^{4}}`.

## Solution

Let \(u=\ln x\), so \(dx=e^{u}\,du\) and the limits run from \(0\) to \(\infty\). The integrand becomes \(u^4 e^{-3u}\). The further substitution \(t=3u\) gives
\[
\int_0^\infty\Bigl(\frac{t}{3}\Bigr)^4 e^{-t}\frac{dt}{3}=\frac{1}{243}\int_0^\infty t^4 e^{-t}\,dt=\frac{4!}{243}=\frac{8}{81}.
\]

## Final answer

The catalog stores `answer_sympy` as `8/81` and `answer_latex` as `\frac{8}{81}`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
