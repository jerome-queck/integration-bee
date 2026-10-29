# YANG-1.8-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 8, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ x/((x+1)(x+2)(x+3)) dx

## Solution

Split the proper fraction as −1/(2(x+1)) + 2/(x+2) − 3/(2(x+3)).

## Final answer

\[
- \frac{\log{\left(\left|{x + 1}\right| \right)}}{2} + 2 \log{\left(\left|{x + 2}\right| \right)} - \frac{3 \log{\left(\left|{x + 3}\right| \right)}}{2}
\]

Stored `answer_sympy`: `-log(Abs(x + 1))/2 + 2*log(Abs(x + 2)) - 3*log(Abs(x + 3))/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
