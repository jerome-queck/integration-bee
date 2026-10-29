# YANG-1.2-P20

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 20, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \csc(1-x)\cot(1-x)\,dx.\]

## Solution

Differentiate \(\csc(1-x)\). With \(u=1-x\), \(\frac{d}{dx}\csc u=(-\csc u\cot u)(-1)=\csc(1-x)\cot(1-x)\). The same function is \(-\csc(x-1)\), because \(\csc\) is odd and \(\cot(1-x)\csc(1-x)=\cot(x-1)\csc(x-1)\).

## Final answer

\[\csc(1-x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `cot(x - 1)*csc(x - 1)` and `answer_sympy` `-csc(x - 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
