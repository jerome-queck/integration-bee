# YANG-2.3-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 10, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ dx/(1+√x)^2.

Catalog integrand `(sqrt(x) + 1)**(-2)`, limits `[]`, display `\frac{1}{\left(\sqrt{x} + 1\right)^{2}}`.

## Solution

Let \(u=\sqrt{x}\), so \(dx=2u\,du\). Then \(u=(1+u)-1\) and
\[
\int\frac{2u}{(1+u)^2}\,du=2\int\Bigl(\frac{1}{1+u}-\frac{1}{(1+u)^2}\Bigr)\,du
=2\ln(1+u)+\frac{2}{1+u}.
\]
Back-substituting gives \(2\ln(1+\sqrt{x})+2/(1+\sqrt{x})\).

## Final answer

The catalog stores `answer_sympy` as `2*log(sqrt(x) + 1) + 2/(sqrt(x) + 1)` and `answer_latex` as `2 \log{\left(\sqrt{x} + 1 \right)} + \frac{2}{\sqrt{x} + 1}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
