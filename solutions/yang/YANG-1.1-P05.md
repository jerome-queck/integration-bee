# YANG-1.1-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.1 Basic Integration, textbook list item 5, printed p. 7 (PDF p. 8).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{4}{1+x^2}\,dx.\]

## Solution

The arctangent derivative gives \(4\arctan x\).

## Final answer

\[4\arctan x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `4/(x**2 + 1)` and `answer_sympy` `4*atan(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
