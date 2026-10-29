# YANG-1.11-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 14, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫_1^(3/2) x^2/(x−2)^3 dx

## Solution

Set u = x−2. On [1, 3/2] this runs from −1 to −1/2, and (u+2)^2/u^3 = 1/u + 4/u^2 + 4/u^3. The evaluated antiderivative is −2 − log 2.

## Final answer

\[
-2 - \log{\left(2 \right)}
\]

Stored `answer_sympy`: `-2 - log(2)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `definite` comparison of the stored fields. The stored value is the exact evaluation of the printed limits. `make check` re-proves those fields. Numeric agreement is not the proof.
