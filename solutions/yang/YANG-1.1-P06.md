# YANG-1.1-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.1 Basic Integration, textbook list item 6, printed p. 7 (PDF p. 8).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{7}{\sqrt{1-x^2}}\,dx.\]

## Solution

The arcsine derivative gives \(7\arcsin x\).

## Final answer

\[7\arcsin x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `7/sqrt(1 - x**2)` and `answer_sympy` `7*asin(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
