# YANG-2.3-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 2, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ sin(ln x) dx.

Catalog integrand `sin(log(x))`, limits `[]`, display `\sin{\left(\log{\left(x \right)} \right)}`.

## Solution

Let \(u=\ln x\), so \(x=e^{u}\) and \(dx=e^{u}\,du\). Then
\[
\int e^{u}\sin u\,du=\frac{e^{u}}{2}(\sin u-\cos u)=\frac{x}{2}\bigl(\sin(\ln x)-\cos(\ln x)\bigr).
\]
The complex form \(\operatorname{Im}\int x^{i}\,dx\) gives the same real antiderivative. Differentiating the stored expression recovers \(\sin(\ln x)\).

## Final answer

The catalog stores `answer_sympy` as `x*sin(log(x))/2 - x*cos(log(x))/2` and `answer_latex` as `\frac{x \sin{\left(\log{\left(x \right)} \right)}}{2} - \frac{x \cos{\left(\log{\left(x \right)} \right)}}{2}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
