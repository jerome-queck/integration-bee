# YANG-1.5-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 9, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\sin x-\cos x}{\sin x+\cos x}\,dx.\]

## Solution

Set \(u=\sin x+\cos x\). Then \(du=(\cos x-\sin x)\,dx\), so the integral is \(-\log(\sin x+\cos x)\).

## Final answer

\[-\log(\sin x+\cos x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(sin(x) - cos(x))/(sin(x) + cos(x))` and `answer_sympy` `-log(sin(x) + cos(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
