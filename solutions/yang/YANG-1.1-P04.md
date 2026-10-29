# YANG-1.1-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.1 Basic Integration, textbook list item 4, printed p. 7 (PDF p. 8).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int 4\sin(x/3)\,dx.\]

## Solution

Let \(u=x/3\). Then \(du=dx/3\), and the integral is \(12\int\sin u\,du=-12\cos(x/3)\).

## Final answer

\[-12\cos(x/3).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `4*sin(x/3)` and `answer_sympy` `-12*cos(x/3)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
