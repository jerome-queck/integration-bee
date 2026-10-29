# YANG-1.2-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 16, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\sin(\ln x)}{x}\,dx.\]

## Solution

Let \(u=\ln x\). Then \(du=dx/x\), so the integral is \(-\cos(\ln x)\).

## Final answer

\[-\cos(\ln x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sin(log(x))/x` and `answer_sympy` `-cos(log(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
