# YANG-1.11-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 3, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ x^3 e^(x^2) dx

## Solution

Set u = x^2. Then x^3 e^(x^2) dx = (1/2) u e^u du, and ∫ u e^u du = e^u(u−1).

## Final answer

\[
\frac{x^{2} e^{x^{2}}}{2} - \frac{e^{x^{2}}}{2}
\]

Stored `answer_sympy`: `x**2*exp(x**2)/2 - exp(x**2)/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
