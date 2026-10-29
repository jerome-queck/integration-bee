# YANG-2.6-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 1, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \sqrt{\cos{\left(x \right)} + 1}\,dx.
\]

## Solution

Use 1 + cos(x) = 2 cos(x/2)^2. Where cos(x/2) > 0 the integrand is sqrt(2) cos(x/2). The gate accepts the antiderivative because its squared derivative matches and the two sides agree at x = 0.

## Final answer

\[
2 \sqrt{2} \sin{\left(\frac{x}{2} \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `sqrt(cos(x) + 1)`. `answer_sympy` is `2*sqrt(2)*sin(x/2)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
