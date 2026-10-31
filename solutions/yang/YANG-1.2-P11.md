# YANG-1.2-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 11, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{1}{\sqrt[3]{x-2024}}\,dx.\]

## Solution

The printed radical is the real reciprocal cube root of \(x-2024\), which is \(\operatorname{sign}(x-2024)/|x-2024|^{1/3}\) for \(x\neq 2024\). Let \(u=x-2024\). The antiderivative is \(\frac32|x-2024|^{2/3}\).

## Final answer

\[\frac32|x-2024|^{2/3}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sign(x - 2024)/Abs(x - 2024)**(1/3)` and `answer_sympy` `3*Abs(x - 2024)**(2/3)/2`. `make check` re-proves that stored pair.
