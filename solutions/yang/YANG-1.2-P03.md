# YANG-1.2-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 3, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (e^x+1)(e^x+x)\,dx.\]

## Solution

Let \(u=e^x+x\). Then \(du=(e^x+1)\,dx\), so the integral is \(\frac12(e^x+x)^2\).

## Final answer

\[\frac12(e^x+x)^2.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(x + exp(x))*(exp(x) + 1)` and `answer_sympy` `x**2/2 + x*exp(x) + exp(2*x)/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
