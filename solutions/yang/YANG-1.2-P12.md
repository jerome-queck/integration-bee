# YANG-1.2-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 12, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^x}{e^{2x}+1}\,dx.\]

## Solution

Let \(u=e^x\). Then \(du=e^x\,dx\), so the integral is \(\arctan(e^x)\).

## Final answer

\[\arctan(e^x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(x)/(exp(2*x) + 1)` and `answer_sympy` `atan(exp(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
