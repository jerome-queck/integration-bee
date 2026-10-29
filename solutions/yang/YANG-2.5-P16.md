# YANG-2.5-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 16, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int x e^{x} \sin{\left(x \right)}\,dx.
\]

## Solution

Tabular integration by parts on x e^x sin(x) produces e^x (x sin(x) - x cos(x) + cos(x))/2.

## Final answer

\[
\frac{x e^{x} \sin{\left(x \right)}}{2} - \frac{x e^{x} \cos{\left(x \right)}}{2} + \frac{e^{x} \cos{\left(x \right)}}{2}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `x*exp(x)*sin(x)`. `answer_sympy` is `x*exp(x)*sin(x)/2 - x*exp(x)*cos(x)/2 + exp(x)*cos(x)/2`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
