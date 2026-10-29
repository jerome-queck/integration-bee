# YANG-2.6-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 16, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \csc{\left(x \right)} \sec{\left(x \right)}\,dx.
\]

## Solution

The derivative of ln|tan(x)| is sec(x) csc(x).

## Final answer

\[
\log{\left(\left|{\tan{\left(x \right)}}\right| \right)}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `csc(x)*sec(x)`. `answer_sympy` is `log(Abs(tan(x)))`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
