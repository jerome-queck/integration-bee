# YANG-2.3-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 14, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ dx/(2√(x+3)+x).

Catalog integrand `1/(x + 2*sqrt(x + 3))`, limits `[]`, display `\frac{1}{x + 2 \sqrt{x + 3}}`.

## Solution

Let \(u=\sqrt{x+3}\), so \(x=u^2-3\) and \(dx=2u\,du\). The denominator is \(u^2+2u-3=(u+3)(u-1)\), and
\[
\int\frac{2u}{(u+3)(u-1)}\,du=\int\Bigl(\frac{3/2}{u+3}+\frac{1/2}{u-1}\Bigr)\,du
=\frac32\ln|u+3|+\frac12\ln|u-1|.
\]
The identity \(x+2\sqrt{x+3}=(u+3)(u-1)\) rewrites that combination as the stored expression
\(\ln(x+2\sqrt{x+3})-\frac12\ln(\sqrt{x+3}-1)+\frac12\ln(\sqrt{x+3}+3)\).

## Final answer

The catalog stores `answer_sympy` as `log(x + 2*sqrt(x + 3)) - log(sqrt(x + 3) - 1)/2 + log(sqrt(x + 3) + 3)/2` and `answer_latex` as `\log{\left(x + 2 \sqrt{x + 3} \right)} - \frac{\log{\left(\sqrt{x + 3} - 1 \right)}}{2} + \frac{\log{\left(\sqrt{x + 3} + 3 \right)}}{2}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
