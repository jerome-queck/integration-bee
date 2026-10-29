# YANG-1.5-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 2, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \sin^{2}x\cos x\,dx.\]

## Solution

Set \(u=\sin x\). Then \(du=\cos x\,dx\), so the integral is \(\sin^{3}x/3\).

## Final answer

\[\dfrac{\sin^{3}x}{3}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sin(x)**2*cos(x)` and `answer_sympy` `sin(x)**3/3`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
