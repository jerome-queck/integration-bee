# YANG-2.5-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 3, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\log{\left(x \right)}^{2}}{x^{3}}\,dx.
\]

## Solution

Integrate by parts twice, taking the power of the logarithm as the differentiated factor.

## Final answer

\[
- \frac{\log{\left(x \right)}^{2}}{2 x^{2}} - \frac{\log{\left(x \right)}}{2 x^{2}} - \frac{1}{4 x^{2}}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `log(x)**2/x**3`. `answer_sympy` is `-log(x)**2/(2*x**2) - log(x)/(2*x**2) - 1/(4*x**2)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
