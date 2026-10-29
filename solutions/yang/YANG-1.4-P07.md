# YANG-1.4-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 7, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int 2^{x-1}e^{x+1}\,dx.\]

## Solution

Differentiating the integrand multiplies it by \(\log 2+1\), because \(\frac{d}{dx}2^{x-1}=2^{x-1}\log 2\) and \(\frac{d}{dx}e^{x+1}=e^{x+1}\). Divide by that constant factor.

## Final answer

\[\dfrac{2^{x-1}e^{x+1}}{\log 2+1}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `2**(x - 1)*exp(x + 1)` and `answer_sympy` `2**x*E*exp(x)/(2*log(2) + 2)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
