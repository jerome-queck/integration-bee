# YANG-2.3-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 15, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ 3^{√(2x+1)} dx.

Catalog integrand `3**(sqrt(2*x + 1))`, limits `[]`, display `3^{\sqrt{2 x + 1}}`.

## Solution

Let \(u=\sqrt{2x+1}\), so \(dx=u\,du\). Integration by parts on \(\int u\,3^{u}\,du\), using \(\int 3^{u}\,du=3^{u}/\ln 3\), gives
\[
3^{u}\Bigl(\frac{u}{\ln 3}-\frac{1}{(\ln 3)^2}\Bigr).
\]
The stored antiderivative is that expression with \(u=\sqrt{2x+1}\). Differentiating it recovers \(3^{\sqrt{2x+1}}\).

## Final answer

The catalog stores `answer_sympy` as `3**(sqrt(2*x + 1))*sqrt(2*x + 1)/log(3) - 3**(sqrt(2*x + 1))/log(3)**2` and `answer_latex` as `\frac{3^{\sqrt{2 x + 1}} \sqrt{2 x + 1}}{\log{\left(3 \right)}} - \frac{3^{\sqrt{2 x + 1}}}{\log{\left(3 \right)}^{2}}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
