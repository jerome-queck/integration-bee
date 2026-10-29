# YANG-2.5-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 6, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{\log{\left(x + 1 \right)}}{x^{\frac{3}{2}}}\,dx.
\]

## Solution

Integrate by parts with u = ln(x+1). The remaining integral, with t = sqrt(x), is 2 arctan(t), and the factor in front makes 4 arctan(sqrt(x)).

## Final answer

\[
4 \operatorname{atan}{\left(\sqrt{x} \right)} - \frac{2 \log{\left(x + 1 \right)}}{\sqrt{x}}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `log(x + 1)/x**(3/2)`. `answer_sympy` is `4*atan(sqrt(x)) - 2*log(x + 1)/sqrt(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
