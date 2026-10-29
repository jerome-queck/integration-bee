# YANG-2.5-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 15, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \log{\left(\sin{\left(x \right)} \right)} \sin{\left(x \right)}\,dx.
\]

## Solution

Integrate by parts with u = ln(sin(x)). The remainder is ∫ csc(x) dx.

## Final answer

\[
- \log{\left(\sin{\left(x \right)} \right)} \cos{\left(x \right)} - \log{\left(\left|{\cot{\left(x \right)} + \csc{\left(x \right)}}\right| \right)} + \cos{\left(x \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `log(sin(x))*sin(x)`. `answer_sympy` is `-log(sin(x))*cos(x) - log(Abs(cot(x) + csc(x))) + cos(x)`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
