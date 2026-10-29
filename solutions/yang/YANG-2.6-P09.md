# YANG-2.6-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 9, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{1}{8 \cos^{2}{\left(x \right)} + 1}\,dx.
\]

## Solution

Rewrite the denominator as 5 + 4 cos(2x). The tangent half-angle substitution produces arctan(tan(x)/3)/3 on (-π/2, π/2).

## Final answer

\[
\frac{\operatorname{atan}{\left(\frac{\tan{\left(x \right)}}{3} \right)}}{3}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `1/(8*cos(x)**2 + 1)`. `answer_sympy` is `atan(tan(x)/3)/3`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
