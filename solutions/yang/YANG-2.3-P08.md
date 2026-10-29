# YANG-2.3-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 8, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫ arctan(√x) dx.

Catalog integrand `atan(sqrt(x))`, limits `[]`, display `\operatorname{atan}{\left(\sqrt{x} \right)}`.

## Solution

Let \(u=\sqrt{x}\), so \(dx=2u\,du\). Integration by parts on \(\int 2u\arctan u\,du\) gives
\[
u^2\arctan u-\int\frac{u^2}{1+u^2}\,du=u^2\arctan u-\int\Bigl(1-\frac{1}{1+u^2}\Bigr)\,du
=(u^2+1)\arctan u-u.
\]
In \(x\) this is \((x+1)\arctan(\sqrt{x})-\sqrt{x}\).

## Final answer

The catalog stores `answer_sympy` as `-sqrt(x) + x*atan(sqrt(x)) + atan(sqrt(x))` and `answer_latex` as `- \sqrt{x} + x \operatorname{atan}{\left(\sqrt{x} \right)} + \operatorname{atan}{\left(\sqrt{x} \right)}`.

## SymPy self-check

`verify/pack_gate.py` proves this indefinite row by differentiating the stored antiderivative. `make check` re-proves the stored fields and does not open the PDF.
