# YANG-2.5-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 11, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\sin{\left(\log{\left(x \right)} \right)}}{x^{3}}\,dx.
\]

## Solution

Set u = ln(x). The integral becomes ∫ e^{-2u} sin(u) du.

## Final answer

\[
- \frac{2 \sin{\left(\log{\left(x \right)} \right)}}{5 x^{2}} - \frac{\cos{\left(\log{\left(x \right)} \right)}}{5 x^{2}}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `sin(log(x))/x**3`. `answer_sympy` is `-2*sin(log(x))/(5*x**2) - cos(log(x))/(5*x**2)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
