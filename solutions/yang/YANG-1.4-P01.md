# YANG-1.4-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 1, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^{x}}{e^{x}+2024}\,dx.\]

## Solution

Set \(u=e^{x}+2024\). Then \(du=e^{x}\,dx\), so the integral is \(\log(e^{x}+2024)\).

## Final answer

\[\log(e^{x}+2024).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(x)/(exp(x) + 2024)` and `answer_sympy` `log(exp(x) + 2024)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
