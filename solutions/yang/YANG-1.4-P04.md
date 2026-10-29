# YANG-1.4-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 4, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{1}{e^{x}+1}\,dx.\]

## Solution

Rewrite the integrand as \(1-e^{x}/(e^{x}+1)\). The integral is \(x-\log(e^{x}+1)\).

## Final answer

\[x-\log(e^{x}+1).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `1/(exp(x) + 1)` and `answer_sympy` `x - log(exp(x) + 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
