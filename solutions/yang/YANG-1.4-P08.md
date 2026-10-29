# YANG-1.4-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 8, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int e^{x}\sin(e^{x})\,dx.\]

## Solution

Set \(u=e^{x}\). Then \(du=e^{x}\,dx\), and \(\int\sin u\,du=-\cos(e^{x})\).

## Final answer

\[-\cos(e^{x}).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(x)*sin(exp(x))` and `answer_sympy` `-cos(exp(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
