# YANG-1.4-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 12, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (e^{x}+1)(e^{-x}+1)\,dx.\]

## Solution

Expand the product as \(2+e^{x}+e^{-x}\). The integral is \(2x+e^{x}-e^{-x}\).

## Final answer

\[2x+e^{x}-e^{-x}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(1 + exp(-x))*(exp(x) + 1)` and `answer_sympy` `2*x + exp(x) - exp(-x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
