# YANG-1.4-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 16, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int e^{e^{x}}(e^{2x}+e^{x})\,dx.\]

## Solution

Set \(u=e^{x}\). Then \(dx=du/u\), and the integrand becomes \(e^{u}(u+1)\,du\). Integration by parts gives \(u e^{u}=e^{x}e^{e^{x}}\).

## Final answer

\[e^{x}e^{e^{x}}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(exp(2*x) + exp(x))*exp(exp(x))` and `answer_sympy` `exp(x)*exp(exp(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
