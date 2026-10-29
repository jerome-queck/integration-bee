# YANG-2.6-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 11, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{2 \tan{\left(x \right)}}{1 - \tan^{2}{\left(x \right)}}\,dx.
\]

## Solution

The integrand is tan(2x), whose antiderivative is -ln|cos(2x)|/2.

## Final answer

\[
- \frac{\log{\left(\left|{\cos{\left(2 x \right)}}\right| \right)}}{2}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `2*tan(x)/(1 - tan(x)**2)`. `answer_sympy` is `-log(Abs(cos(2*x)))/2`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
