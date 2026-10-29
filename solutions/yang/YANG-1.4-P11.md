# YANG-1.4-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 11, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^{x}+e^{2x}}{1+e^{2x}}\,dx.\]

## Solution

Set \(u=e^{x}\). The integral becomes \(\int(1+u)/(1+u^{2})\,du=\arctan(e^{x})+\frac12\log(1+e^{2x})\).

## Final answer

\[\arctan(e^{x})+\dfrac{1}{2}\log(1+e^{2x}).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(exp(2*x) + exp(x))/(exp(2*x) + 1)` and `answer_sympy` `log(exp(2*x) + 1)/2 + atan(exp(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
