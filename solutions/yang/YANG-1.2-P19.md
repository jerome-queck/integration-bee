# YANG-1.2-P19

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 19, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \left(1+\frac1x\right)\ln(xe^x)\,dx.\]

## Solution

\(\ln(xe^x)=x+\ln x\), and the derivative of that sum is \(1+1/x\). Let \(u=x+\ln x\). The integral is \(\frac12(x+\ln x)^2\).

## Final answer

\[\frac12(x+\ln x)^2.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(1 + 1/x)*log(x*exp(x))` and `answer_sympy` `x**2/2 + x*log(x) + log(x)**2/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
