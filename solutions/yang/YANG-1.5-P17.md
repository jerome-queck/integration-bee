# YANG-1.5-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 17, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\tan x+1}{\sec x}\,dx.\]

## Solution

The integrand is \(\sin x+\cos x\). The integral is \(\sin x-\cos x\).

## Final answer

\[\sin x-\cos x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(tan(x) + 1)/sec(x)` and `answer_sympy` `sin(x) - cos(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
