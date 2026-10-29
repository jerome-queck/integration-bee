# YANG-1.5-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 3, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \sin^{2}x\cos^{3}x\,dx.\]

## Solution

Write \(\cos^{3}x=\cos x(1-\sin^{2}x)\). Set \(u=\sin x\). The integral is \(\sin^{3}x/3-\sin^{5}x/5\).

## Final answer

\[\dfrac{\sin^{3}x}{3}-\dfrac{\sin^{5}x}{5}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sin(x)**2*cos(x)**3` and `answer_sympy` `-sin(x)**5/5 + sin(x)**3/3`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
