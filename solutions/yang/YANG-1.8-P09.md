# YANG-1.8-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 9, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ dx/(x^2(1+x^2))

## Solution

Write 1/(x^2(1+x^2)) as 1/x^2 − 1/(1+x^2).

## Final answer

\[
- \operatorname{atan}{\left(x \right)} - \frac{1}{x}
\]

Stored `answer_sympy`: `-atan(x) - 1/x`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
