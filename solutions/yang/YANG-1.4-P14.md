# YANG-1.4-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 14, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{e^{x}}{(e^{x}-1)\ln(e^{x}-1)}\,dx.\]

## Solution

Set \(u=\ln(e^{x}-1)\). Then \(du=e^{x}/(e^{x}-1)\,dx\), so the integral is \(\log(\ln(e^{x}-1))\).

## Final answer

\[\log(\ln(e^{x}-1)).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `exp(x)/((exp(x) - 1)*log(exp(x) - 1))` and `answer_sympy` `log(log(exp(x) - 1))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
