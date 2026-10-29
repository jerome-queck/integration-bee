# YANG-1.11-P20

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 20, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ (ln x+1)/(x ln x+1) dx

## Solution

The derivative of x ln x + 1 is ln x + 1, so the integrand is the logarithmic derivative of the denominator.

## Final answer

\[
\log{\left(\left|{x \log{\left(x \right)} + 1}\right| \right)}
\]

Stored `answer_sympy`: `log(Abs(x*log(x) + 1))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
