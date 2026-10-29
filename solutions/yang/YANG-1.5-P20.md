# YANG-1.5-P20

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 20, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\sin x+\cos x}{\sec x+\csc x}\,dx.\]

## Solution

\(\sec x+\csc x=(\sin x+\cos x)/(\sin x\cos x)\), so the integrand simplifies to \(\sin x\cos x\). The integral is \(\sin^{2}x/2\).

## Final answer

\[\dfrac{\sin^{2}x}{2}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(sin(x) + cos(x))/(csc(x) + sec(x))` and `answer_sympy` `sin(x)**2/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
