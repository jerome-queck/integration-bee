# YANG-1.2-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 10, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (x+1)^{2024}\,dx.\]

## Solution

Let \(u=x+1\). The integral is \((x+1)^{2025}/2025\).

## Final answer

\[\frac{(x+1)^{2025}}{2025}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(x + 1)**2024` and `answer_sympy` `(x + 1)**2025/2025`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
