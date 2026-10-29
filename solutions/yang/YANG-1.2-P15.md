# YANG-1.2-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 15, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (x+1)e^{x^2+2x}\,dx.\]

## Solution

Let \(u=x^2+2x\). Then \(du=2(x+1)\,dx\), so the integral is \(\frac12 e^{x^2+2x}\).

## Final answer

\[\frac12 e^{x^2+2x}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(x + 1)*exp(x**2 + 2*x)` and `answer_sympy` `exp(2*x)*exp(x**2)/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
