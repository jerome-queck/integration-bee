# YANG-1.4-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 5, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^{x}+1}{x+e^{x}+1}\,dx.\]

## Solution

The numerator is the derivative of the denominator, so the integral is \(\log(x+e^{x}+1)\).

## Final answer

\[\log(x+e^{x}+1).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(exp(x) + 1)/(x + exp(x) + 1)` and `answer_sympy` `log(x + exp(x) + 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
