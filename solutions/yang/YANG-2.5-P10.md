# YANG-2.5-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 10, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{x e^{x}}{\sqrt{e^{x} - 1}}\,dx.
\]

## Solution

Set t = sqrt(e^x - 1). Then t^2 + 1 = e^x and the integral becomes 2 ∫ ln(t^2+1) dt.

## Final answer

\[
2 x \sqrt{e^{x} - 1} - 4 \sqrt{e^{x} - 1} + 4 \operatorname{atan}{\left(\sqrt{e^{x} - 1} \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `x*exp(x)/sqrt(exp(x) - 1)`. `answer_sympy` is `2*x*sqrt(exp(x) - 1) - 4*sqrt(exp(x) - 1) + 4*atan(sqrt(exp(x) - 1))`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
