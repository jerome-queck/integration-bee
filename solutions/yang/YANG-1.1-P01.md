# YANG-1.1-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.1 Basic Integration, textbook list item 1, printed p. 7 (PDF p. 8).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (5x^2-8x+5)\,dx.\]

## Solution

Each term is a power. The antiderivative is \(\frac{5}{3}x^3-4x^2+5x\).

## Final answer

\[\frac{5}{3}x^3-4x^2+5x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `5*x**2 - 8*x + 5` and `answer_sympy` `5*x**3/3 - 4*x**2 + 5*x`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
