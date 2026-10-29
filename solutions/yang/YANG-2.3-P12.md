# YANG-2.3-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 12, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ dx/√(2021^x-1).

Catalog integrand `1/sqrt(2021**x - 1)`, limits `[]`, display `\frac{1}{\sqrt{2021^{x} - 1}}`.

## Solution

Let \(v=\sqrt{2021^x-1}\), so \(2021^x=v^2+1\) and \(2021^x\ln 2021\,dx=2v\,dv\). Then
\[
dx=\frac{2v\,dv}{(v^2+1)\ln 2021},\qquad
\int\frac{dx}{v}=\int\frac{2\,dv}{(v^2+1)\ln 2021}=\frac{2}{\ln 2021}\arctan v.
\]
The antiderivative is \(2\arctan(\sqrt{2021^x-1})/\ln 2021\). Differentiating it recovers the integrand.

## Final answer

The catalog stores `answer_sympy` as `2*atan(sqrt(2021**x - 1))/log(2021)` and `answer_latex` as `\frac{2 \operatorname{atan}{\left(\sqrt{2021^{x} - 1} \right)}}{\log{\left(2021 \right)}}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
