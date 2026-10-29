# YANG-2.6-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 7, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\cos{\left(2 x \right)}}{\sin{\left(x \right)} + \cos{\left(x \right)}}\,dx.
\]

## Solution

cos(2x) = (cos(x)-sin(x))(cos(x)+sin(x)), so the integrand simplifies to cos(x)-sin(x) wherever sin(x)+cos(x) is not zero.

## Final answer

\[
\sin{\left(x \right)} + \cos{\left(x \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `cos(2*x)/(sin(x) + cos(x))`. `answer_sympy` is `sin(x) + cos(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
