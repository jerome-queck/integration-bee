# YANG-2.5-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 7, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\operatorname{atan}{\left(x \right)}}{x^{2}}\,dx.
\]

## Solution

Integrate by parts with u = arctan(x). Partial fractions give 1/(x(1+x^2)) = 1/x - x/(1+x^2).

## Final answer

\[
- \frac{\log{\left(x^{2} + 1 \right)}}{2} + \log{\left(\left|{x}\right| \right)} - \frac{\operatorname{atan}{\left(x \right)}}{x}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `atan(x)/x**2`. `answer_sympy` is `-log(x**2 + 1)/2 + log(Abs(x)) - atan(x)/x`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
