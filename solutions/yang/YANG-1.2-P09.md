# YANG-1.2-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 9, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (x^2+x+1)(2x+1)\,dx.\]

## Solution

Let \(u=x^2+x+1\). Then \(du=(2x+1)\,dx\), so the integral is \(\frac12(x^2+x+1)^2\).

## Final answer

\[\frac12(x^2+x+1)^2.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(2*x + 1)*(x**2 + x + 1)` and `answer_sympy` `x**4/2 + x**3 + 3*x**2/2 + x + 1/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
