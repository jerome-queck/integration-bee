# YANG-1.8-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 4, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ dx/(x(2x−1))

## Solution

Split 1/(x(2x−1)) as −1/x + 2/(2x−1).

## Final answer

\[
- \log{\left(\left|{x}\right| \right)} + \log{\left(\left|{2 x - 1}\right| \right)}
\]

Stored `answer_sympy`: `-log(Abs(x)) + log(Abs(2*x - 1))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
