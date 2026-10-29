# YANG-1.2-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 7, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \sec^2(5x-4)\,dx.\]

## Solution

Let \(u=5x-4\). Then \(du=5\,dx\), so the integral is \(\frac15\tan(5x-4)\). That quotient is \(\sin(5x-4)/(5\cos(5x-4))\). The catalog stores the sine-over-cosine form: differentiating \(\tan(5x-4)\) through SymPy produces \(1+\tan^2(5x-4)\), and the gate's comparison with \(\sec^2(5x-4)\) does not cancel that identity, while the quotient's derivative matches \(\sec^2(5x-4)\) exactly. The two expressions differ by the zero function.

## Final answer

\[\frac15\tan(5x-4).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sec(5*x - 4)**2` and `answer_sympy` `sin(5*x - 4)/(5*cos(5*x - 4))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
