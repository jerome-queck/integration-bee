# YANG-2.6-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 2, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\sec{\left(x \right)}}{- \tan{\left(x \right)} + \sec{\left(x \right)}}\,dx.
\]

## Solution

Multiply numerator and denominator by sec(x)+tan(x). The integrand is the derivative of sec(x)+tan(x).

## Final answer

\[
\tan{\left(x \right)} + \sec{\left(x \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `sec(x)/(-tan(x) + sec(x))`. `answer_sympy` is `tan(x) + sec(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
