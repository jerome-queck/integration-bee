# YANG-2.5-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 2, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int e^{x} \sin{\left(x \right)} \cos{\left(x \right)}\,dx.
\]

## Solution

Use sin(x) cos(x) = sin(2x)/2, then the formula for ∫ e^{ax} sin(bx) dx with a = 1 and b = 2.

## Final answer

\[
\frac{e^{x} \sin{\left(2 x \right)}}{10} - \frac{e^{x} \cos{\left(2 x \right)}}{5}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `exp(x)*sin(x)*cos(x)`. `answer_sympy` is `exp(x)*sin(2*x)/10 - exp(x)*cos(2*x)/5`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
