# YANG-1.5-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 8, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\csc x\cot x}{1+\csc x}\,dx.\]

## Solution

Set \(u=\csc x\). Then \(du=-\csc x\cot x\,dx\), so the integral is \(-\log(1+\csc x)\).

## Final answer

\[-\log(1+\csc x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `cot(x)*csc(x)/(csc(x) + 1)` and `answer_sympy` `-log(csc(x) + 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
