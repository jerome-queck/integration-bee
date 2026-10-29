# YANG-2.6-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 4, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \sin^{3}{\left(x \right)} + \cos^{3}{\left(x \right)}\,dx.
\]

## Solution

Write sin(x)^3 = sin(x)(1-cos(x)^2) and cos(x)^3 = cos(x)(1-sin(x)^2), then integrate termwise.

## Final answer

\[
- \frac{\sin^{3}{\left(x \right)}}{3} + \sin{\left(x \right)} + \frac{\cos^{3}{\left(x \right)}}{3} - \cos{\left(x \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `sin(x)**3 + cos(x)**3`. `answer_sympy` is `-sin(x)**3/3 + sin(x) + cos(x)**3/3 - cos(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
