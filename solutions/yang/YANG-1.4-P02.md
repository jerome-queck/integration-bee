# YANG-1.4-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 2, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^{x}}{(e^{x}+1)^{2}}\,dx.\]

## Solution

Set \(u=e^{x}+1\). Then \(du=e^{x}\,dx\), so the integral is \(-1/(e^{x}+1)\).

## Final answer

\[-\dfrac{1}{e^{x}+1}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(x)/(exp(x) + 1)**2` and `answer_sympy` `-1/(exp(x) + 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
