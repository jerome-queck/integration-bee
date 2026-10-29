# YANG-1.5-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 10, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \sin^{3}x\,dx.\]

## Solution

Write \(\sin^{3}x=(1-\cos^{2}x)\sin x\). Set \(u=\cos x\). The integral is \(-\cos x+\cos^{3}x/3\).

## Final answer

\[-\cos x+\dfrac{\cos^{3}x}{3}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sin(x)**3` and `answer_sympy` `cos(x)**3/3 - cos(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
