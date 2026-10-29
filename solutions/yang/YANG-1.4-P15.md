# YANG-1.4-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 15, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int\left(\frac{e^{x}}{\cos(e^{2x})}\right)^{2}\,dx.\]

## Solution

The integrand is \(e^{2x}\sec^{2}(e^{2x})\). Set \(u=e^{2x}\), so \(du=2e^{2x}\,dx\). The integral is \(\frac12\tan(e^{2x})\).

## Final answer

\[\dfrac{1}{2}\tan(e^{2x}).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(2*x)/cos(exp(2*x))**2` and `answer_sympy` `tan(exp(2*x))/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
