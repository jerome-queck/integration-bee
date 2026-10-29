# YANG-2.5-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 9, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{x \operatorname{asin}{\left(x \right)}}{\sqrt{1 - x^{2}}}\,dx.
\]

## Solution

The substitution x = sin(u) reduces the integral to ∫ u sin(u) du on the range where cos(u) = sqrt(1-x^2).

## Final answer

\[
x - \sqrt{1 - x^{2}} \operatorname{asin}{\left(x \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `x*asin(x)/sqrt(1 - x**2)`. `answer_sympy` is `x - sqrt(1 - x**2)*asin(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
