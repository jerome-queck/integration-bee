# YANG-1.11-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 15, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ √(sin x)/(cos^2(x) √(cos x)) dx

## Solution

The integrand is sin(x)^(1/2) cos(x)^(−5/2). The derivative of (2/3) sin(x)^(3/2)/cos(x)^(3/2) matches that expression.

## Final answer

\[
\frac{2 \sin^{\frac{3}{2}}{\left(x \right)}}{3 \cos^{\frac{3}{2}}{\left(x \right)}}
\]

Stored `answer_sympy`: `2*sin(x)**(3/2)/(3*cos(x)**(3/2))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
