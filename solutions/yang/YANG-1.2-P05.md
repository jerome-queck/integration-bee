# YANG-1.2-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 5, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int x\sqrt{x-1}\sqrt{x+1}\,dx.\]

## Solution

The printed integrand is the product of the two square roots, not the square root of the product. Differentiate \(\frac13(x-1)^{3/2}(x+1)^{3/2}\): the product rule produces \(\frac12\sqrt{x-1}\sqrt{x+1}\bigl((x+1)+(x-1)\bigr)=x\sqrt{x-1}\sqrt{x+1}\). That antiderivative equals \((x^2-1)\sqrt{x-1}\sqrt{x+1}/3\).

## Final answer

\[\frac13(x-1)^{3/2}(x+1)^{3/2}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `x*sqrt(x - 1)*sqrt(x + 1)` and `answer_sympy` `x**2*sqrt(x - 1)*sqrt(x + 1)/3 - sqrt(x - 1)*sqrt(x + 1)/3`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
