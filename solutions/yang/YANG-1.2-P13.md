# YANG-1.2-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 13, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\cos x+1+e^x}{\sin x+x+e^x}\,dx.\]

## Solution

Let \(u=\sin x+x+e^x\). Then \(du=(\cos x+1+e^x)\,dx\), so the integral is \(\ln|\sin x+x+e^x|\).

## Final answer

\[\ln|\sin x+x+e^x|.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(exp(x) + cos(x) + 1)/(x + exp(x) + sin(x))` and `answer_sympy` `log(Abs(x + exp(x) + sin(x)))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
