# YANG-2.5-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 17, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\log{\left(x^{4} + 1 \right)}}{x^{3}}\,dx.
\]

## Solution

Integrate by parts. The remainder is 2 ∫ x/(1+x^4) dx, and u = x^2 turns that into arctan(x^2).

## Final answer

\[
\operatorname{atan}{\left(x^{2} \right)} - \frac{\log{\left(x^{4} + 1 \right)}}{2 x^{2}}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `log(x**4 + 1)/x**3`. `answer_sympy` is `atan(x**2) - log(x**4 + 1)/(2*x**2)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
