# YANG-2.6-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 8, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \cos{\left(x \right)} \sqrt{\cos{\left(2 x \right)}}\,dx.
\]

## Solution

The substitution u = sin(x) produces ∫ sqrt(1-2u^2) du.

## Final answer

\[
\frac{\sin{\left(x \right)} \sqrt{\cos{\left(2 x \right)}}}{2} + \frac{\sqrt{2} \operatorname{asin}{\left(\sqrt{2} \sin{\left(x \right)} \right)}}{4}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `cos(x)*sqrt(cos(2*x))`. `answer_sympy` is `sin(x)*sqrt(cos(2*x))/2 + sqrt(2)*asin(sqrt(2)*sin(x))/4`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
