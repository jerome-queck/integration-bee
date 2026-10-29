# YANG-1.8-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 17, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫_3^∞ dx/((x−2)(x+6))

## Solution

Split as (1/8)(1/(x−2) − 1/(x+6)). The antiderivative (1/8) log|(x−2)/(x+6)| tends to 0 at infinity and equals −(1/4) log 3 at 3.

## Final answer

\[
\frac{\log{\left(3 \right)}}{4}
\]

Stored `answer_sympy`: `log(3)/4`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `definite` comparison of the stored fields. The stored value is the exact evaluation of the printed limits. `make check` re-proves those fields. Numeric agreement is not the proof.
