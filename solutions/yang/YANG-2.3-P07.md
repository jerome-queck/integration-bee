# YANG-2.3-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 7, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^8 dx/√(1+√(1+x)).

Catalog integrand `1/sqrt(sqrt(x + 1) + 1)`, limits `['0', '8']`, display `\frac{1}{\sqrt{\sqrt{x + 1} + 1}}`.

## Solution

Let \(u=\sqrt{1+x}\), so \(dx=2u\,du\). The limits \(x=0\) and \(x=8\) become \(u=1\) and \(u=3\). Then let \(t=1+u\), running from \(2\) to \(4\):
\[
\int_1^3\frac{2u}{\sqrt{1+u}}\,du=2\int_2^4\bigl(t^{1/2}-t^{-1/2}\bigr)\,dt
=2\Bigl[\frac23 t^{3/2}-2t^{1/2}\Bigr]_2^4=\frac83+\frac{4\sqrt{2}}{3}.
\]

## Final answer

The catalog stores `answer_sympy` as `4*sqrt(2)/3 + 8/3` and `answer_latex` as `\frac{4 \sqrt{2}}{3} + \frac{8}{3}`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
