# YANG-1.4-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 10, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^{x}}{\sqrt{1-e^{2x}}}\,dx.\]

## Solution

Set \(u=e^{x}\). Then \(du=e^{x}\,dx\), and \(\int du/\sqrt{1-u^{2}}=\arcsin(e^{x})\).

## Final answer

\[\arcsin(e^{x}).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(x)/sqrt(1 - exp(2*x))` and `answer_sympy` `asin(exp(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
