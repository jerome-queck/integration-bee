# YANG-1.8-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 7, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ dx/(x^3−x)

## Solution

Factor x^3−x as x(x−1)(x+1) and split as −1/x + (1/2)/(x−1) + (1/2)/(x+1).

## Final answer

\[
- \log{\left(\left|{x}\right| \right)} + \frac{\log{\left(\left|{x - 1}\right| \right)}}{2} + \frac{\log{\left(\left|{x + 1}\right| \right)}}{2}
\]

Stored `answer_sympy`: `-log(Abs(x)) + log(Abs(x - 1))/2 + log(Abs(x + 1))/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
