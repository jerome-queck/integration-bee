# YANG-2.3-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 3, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^1 (1+√x)^8 dx.

Catalog integrand `(sqrt(x) + 1)**8`, limits `['0', '1']`, display `\left(\sqrt{x} + 1\right)^{8}`.

## Solution

Let \(u=\sqrt{x}\), so \(dx=2u\,du\), with limits \(0\) to \(1\). Then
\[
2\int_0^1 u(1+u)^8\,du=2\int_0^1\bigl((1+u)^9-(1+u)^8\bigr)\,du
=2\Bigl[\frac{(1+u)^{10}}{10}-\frac{(1+u)^9}{9}\Bigr]_0^1.
\]
The upper endpoint is \(2(2^{10}/10-2^9/9)=2(1024/10-512/9)\). Subtracting the lower endpoint \(2(1/10-1/9)\) leaves \(4097/45\).

## Final answer

The catalog stores `answer_sympy` as `4097/45` and `answer_latex` as `\frac{4097}{45}`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
