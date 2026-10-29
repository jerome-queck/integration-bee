# YANG-2.3-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 17, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ x ln(x)^5 dx.

Catalog integrand `x*log(x)**5`, limits `[]`, display `x \log{\left(x \right)}^{5}`.

## Solution

Integrate by parts with \(v=\ln^5 x\) and \(dw=x\,dx\), so \(w=x^2/2\). Each step lowers the power of the logarithm:
\[
\int x\ln^n x\,dx=\frac{x^2}{2}\ln^n x-\frac{n}{2}\int x\ln^{n-1}x\,dx.
\]
Carrying this from \(n=5\) down to \(n=0\) produces
\[
\frac{x^2}{2}\ln^5 x-\frac{5x^2}{4}\ln^4 x+\frac{5x^2}{2}\ln^3 x-\frac{15x^2}{4}\ln^2 x+\frac{15x^2}{4}\ln x-\frac{15x^2}{8}.
\]

## Final answer

The catalog stores `answer_sympy` as `x**2*log(x)**5/2 - 5*x**2*log(x)**4/4 + 5*x**2*log(x)**3/2 - 15*x**2*log(x)**2/4 + 15*x**2*log(x)/4 - 15*x**2/8` and `answer_latex` as `\frac{x^{2} \log{\left(x \right)}^{5}}{2} - \frac{5 x^{2} \log{\left(x \right)}^{4}}{4} + \frac{5 x^{2} \log{\left(x \right)}^{3}}{2} - \frac{15 x^{2} \log{\left(x \right)}^{2}}{4} + \frac{15 x^{2} \log{\left(x \right)}}{4} - \frac{15 x^{2}}{8}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
