# YANG-1.11-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 4, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ x/(√x−1) dx

## Solution

Set u = √x. Then the integrand is 2u^3/(u−1) du. Divide to get u^2+u+1+1/(u−1).

## Final answer

\[
\frac{2 x^{\frac{3}{2}}}{3} + 2 \sqrt{x} + x + 2 \log{\left(\left|{\sqrt{x} - 1}\right| \right)}
\]

Stored `answer_sympy`: `2*x**(3/2)/3 + 2*sqrt(x) + x + 2*log(Abs(sqrt(x) - 1))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
