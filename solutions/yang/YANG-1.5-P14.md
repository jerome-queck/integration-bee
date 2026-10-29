# YANG-1.5-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 14, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (\sin x+1)(\cos x+1)\,dx.\]

## Solution

Expand as \(\sin x\cos x+\sin x+\cos x+1\). The product \(\sin x\cos x\) integrates to \(\sin^{2}x/2\), so the integral is \(x+\sin x-\cos x+\sin^{2}x/2\).

## Final answer

\[x+\sin x-\cos x+\dfrac{\sin^{2}x}{2}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(sin(x) + 1)*(cos(x) + 1)` and `answer_sympy` `x + sin(x)**2/2 + sin(x) - cos(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
