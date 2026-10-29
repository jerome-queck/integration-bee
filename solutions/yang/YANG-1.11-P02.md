# YANG-1.11-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 2, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ dx/(√x(1+x))

## Solution

Set u = √x. Then dx = 2u du and the integral is 2 ∫ du/(1+u^2).

## Final answer

\[
2 \operatorname{atan}{\left(\sqrt{x} \right)}
\]

Stored `answer_sympy`: `2*atan(sqrt(x))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
