# YANG-1.5-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 12, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (\sin x+\cos x)^{2}\,dx.\]

## Solution

Expand as \(1+\sin 2x\). The integral is \(x-\cos(2x)/2\).

## Final answer

\[x-\dfrac{\cos 2x}{2}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(sin(x) + cos(x))**2` and `answer_sympy` `x - cos(2*x)/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
