# YANG-1.11-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 13, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ e^(2x)/(1+e^(4x)) dx

## Solution

Set u = e^(2x). Then du = 2 e^(2x) dx, and the integral is (1/2) ∫ du/(1+u^2).

## Final answer

\[
\frac{\operatorname{atan}{\left(e^{2 x} \right)}}{2}
\]

Stored `answer_sympy`: `atan(exp(2*x))/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
