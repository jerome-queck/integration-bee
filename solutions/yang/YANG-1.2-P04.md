# YANG-1.2-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 4, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \sin(\sin x+1)\cos x\,dx.\]

## Solution

Let \(u=\sin x+1\). Then \(du=\cos x\,dx\), so the integral is \(-\cos(\sin x+1)\).

## Final answer

\[-\cos(\sin x+1).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sin(sin(x) + 1)*cos(x)` and `answer_sympy` `-cos(sin(x) + 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
