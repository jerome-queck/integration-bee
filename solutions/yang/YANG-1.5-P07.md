# YANG-1.5-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 7, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\cos x}{\sin^{2}x+1}\,dx.\]

## Solution

Set \(u=\sin x\). Then \(du=\cos x\,dx\), so the integral is \(\arctan(\sin x)\).

## Final answer

\[\arctan(\sin x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `cos(x)/(sin(x)**2 + 1)` and `answer_sympy` `atan(sin(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
