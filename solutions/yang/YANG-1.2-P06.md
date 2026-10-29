# YANG-1.2-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 6, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int e^{x+e^x}\,dx.\]

## Solution

Write the integrand as \(e^x e^{e^x}\). Let \(u=e^x\). Then \(du=e^x\,dx\), and the integral is \(e^{e^x}\).

## Final answer

\[e^{e^x}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(x + exp(x))` and `answer_sympy` `exp(exp(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
