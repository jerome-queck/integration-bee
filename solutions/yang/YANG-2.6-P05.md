# YANG-2.6-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 5, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int - \sin{\left(x + \frac{\pi}{4} \right)} \cos{\left(x + \frac{\pi}{4} \right)}\,dx.
\]

## Solution

The product identity gives sin(x+π/4) sin(x-π/4) = -cos(2x)/2.

## Final answer

\[
- \frac{\sin{\left(2 x \right)}}{4}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `-sin(x + pi/4)*cos(x + pi/4)`. `answer_sympy` is `-sin(2*x)/4`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
