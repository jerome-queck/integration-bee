# YANG-1.8-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 6, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ (x+2)/(x^2+4x+3) dx

## Solution

The denominator is (x+1)(x+3), and the numerator is half of its derivative, so the integral is (1/2) log|x^2+4x+3|.

## Final answer

\[
\frac{\log{\left(\left|{x^{2} + 4 x + 3}\right| \right)}}{2}
\]

Stored `answer_sympy`: `log(Abs(x**2 + 4*x + 3))/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
