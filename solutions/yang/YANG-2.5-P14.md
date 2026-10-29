# YANG-2.5-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 14, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{x \log{\left(x \right)}}{\sqrt{x^{2} - 1}}\,dx.
\]

## Solution

Integrate by parts with dv = x/sqrt(x^2-1) dx. For x > 1 the remaining integral is sqrt(x^2-1) - arcsec(x).

## Final answer

\[
\sqrt{x^{2} - 1} \log{\left(x \right)} - \sqrt{x^{2} - 1} + \operatorname{asec}{\left(x \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `x*log(x)/sqrt(x**2 - 1)`. `answer_sympy` is `sqrt(x**2 - 1)*log(x) - sqrt(x**2 - 1) + asec(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
