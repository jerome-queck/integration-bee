# YANG-1.8-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 16, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫_2^4 (x−4)/(x^2−6x+5) dx

## Solution

On [2, 4] the denominator (x−1)(x−5) has no root. Split as (3/4)/(x−1) + (1/4)/(x−5) and evaluate the logs at the printed endpoints.

## Final answer

\[
\frac{\log{\left(3 \right)}}{2}
\]

Stored `answer_sympy`: `log(3)/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `definite` comparison of the stored fields. The stored value is the exact evaluation of the printed limits. `make check` re-proves those fields. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
