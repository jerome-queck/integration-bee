# YANG-1.1-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.1 Basic Integration, textbook list item 2, printed p. 7 (PDF p. 8).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (e^x+x+e^{-x})\,dx.\]

## Solution

Integrate termwise. \(\int e^{-x}\,dx=-e^{-x}\), so the antiderivative is \(e^x+\frac{1}{2}x^2-e^{-x}\).

## Final answer

\[e^x+\frac12 x^2-e^{-x}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `x + exp(x) + exp(-x)` and `answer_sympy` `x**2/2 + exp(x) - exp(-x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
