# YANG-1.2-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 14, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\sin x\cos x}{\sin^2 x+1}\,dx.\]

## Solution

Let \(u=\sin^2 x\). Then \(du=2\sin x\cos x\,dx\), so the integral is \(\frac12\ln(\sin^2 x+1)\).

## Final answer

\[\frac12\ln(\sin^2 x+1).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sin(x)*cos(x)/(sin(x)**2 + 1)` and `answer_sympy` `log(sin(x)**2 + 1)/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
