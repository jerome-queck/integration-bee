# YANG-2.6-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 6, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\cos{\left(x \right)}}{\cos{\left(2 x \right)} - 1}\,dx.
\]

## Solution

cos(2x) - 1 = -2 sin(x)^2. The substitution u = sin(x) gives 1/(2 sin(x)).

## Final answer

\[
\frac{1}{2 \sin{\left(x \right)}}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `cos(x)/(cos(2*x) - 1)`. `answer_sympy` is `1/(2*sin(x))`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
