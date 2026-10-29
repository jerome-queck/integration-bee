# YANG-2.5-P18

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 18, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \log{\left(\tan{\left(x \right)} \right)} \cos{\left(2 x \right)}\,dx.
\]

## Solution

The derivative of sin(x) cos(x) is cos(2x), and the derivative of ln(tan(x)) is 1/(sin(x) cos(x)). Parts leaves the remainder x.

## Final answer

\[
- x + \log{\left(\tan{\left(x \right)} \right)} \sin{\left(x \right)} \cos{\left(x \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `log(tan(x))*cos(2*x)`. `answer_sympy` is `-x + log(tan(x))*sin(x)*cos(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
