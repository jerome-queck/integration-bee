# YANG-1.4-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 13, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{1}{e^{x}+e^{-x}}\,dx.\]

## Solution

Multiply numerator and denominator by \(e^{x}\) to get \(e^{x}/(e^{2x}+1)\). Set \(u=e^{x}\). The integral is \(\arctan(e^{x})\).

## Final answer

\[\arctan(e^{x}).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `1/(exp(x) + exp(-x))` and `answer_sympy` `atan(exp(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
