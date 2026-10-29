# YANG-1.4-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 6, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (e^{x}+e^{-x})^{4}\,dx.\]

## Solution

Expand \((e^{x}+e^{-x})^{2}=e^{2x}+2+e^{-2x}\) and square again: \(e^{4x}+4e^{2x}+6+4e^{-2x}+e^{-4x}\). Integrate term by term.

## Final answer

\[\dfrac{e^{4x}}{4}-\dfrac{e^{-4x}}{4}+2e^{2x}-2e^{-2x}+6x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(exp(x) + exp(-x))**4` and `answer_sympy` `6*x + exp(4*x)/4 + 2*exp(2*x) - 2*exp(-2*x) - exp(-4*x)/4`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
