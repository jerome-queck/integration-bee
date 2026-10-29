# YANG-1.4-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 9, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^{7x}+e^{4x}}{e^{5x}+e^{2x}}\,dx.\]

## Solution

Factor \(e^{4x}(e^{3x}+1)\) in the numerator and \(e^{2x}(e^{3x}+1)\) in the denominator. The quotient is \(e^{2x}\), whose integral is \(e^{2x}/2\).

## Final answer

\[\dfrac{e^{2x}}{2}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x))` and `answer_sympy` `exp(2*x)/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
