# YANG-1.4-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 17, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int\sqrt{e^{x}\sqrt{e^{x}}}\,dx.\]

## Solution

\(e^{x}\sqrt{e^{x}}=e^{3x/2}\), so the outer square root is \(e^{3x/4}\). The integral is \(\frac43 e^{3x/4}\).

## Final answer

\[\dfrac{4}{3}e^{3x/4}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(3*x/4)` and `answer_sympy` `4*exp(3*x/4)/3`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
