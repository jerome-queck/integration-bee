# YANG-2.5-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 4, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{x}{\sin{\left(x \right)} + 1}\,dx.
\]

## Solution

Multiply numerator and denominator by 1 - sin(x). The integrand becomes x (sec(x)^2 - sec(x) tan(x)). Parts then produces x (tan(x) - sec(x)) plus ln|sec(x)+tan(x)| - ln|sec(x)|.

## Final answer

\[
x \tan{\left(x \right)} - x \sec{\left(x \right)} + \log{\left(\left|{\tan{\left(x \right)} + \sec{\left(x \right)}}\right| \right)} - \log{\left(\left|{\sec{\left(x \right)}}\right| \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `x/(sin(x) + 1)`. `answer_sympy` is `x*tan(x) - x*sec(x) + log(Abs(tan(x) + sec(x))) - log(Abs(sec(x)))`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
