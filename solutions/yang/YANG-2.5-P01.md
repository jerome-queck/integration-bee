# YANG-2.5-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 1, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int x \log{\left(x + 1 \right)}\,dx.
\]

## Solution

Integrate by parts with u = ln(x+1) and dv = x dx. The remaining quotient x^2/(x+1) is x - 1 + 1/(x+1).

## Final answer

\[
\frac{x^{2} \log{\left(x + 1 \right)}}{2} - \frac{x^{2}}{4} + \frac{x}{2} - \frac{\log{\left(x + 1 \right)}}{2}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `x*log(x + 1)`. `answer_sympy` is `x**2*log(x + 1)/2 - x**2/4 + x/2 - log(x + 1)/2`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
