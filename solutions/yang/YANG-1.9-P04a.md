# YANG-1.9-P04a

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.9 Area of a Partial Circle, Hidden Symmetry, printed p. 16 (PDF p. 17).
- Printed answer: \(\pi\).
- Worked source: the guide prints this final. The gate re-proves it.

## Problem

\[
\int_{-2}^{2}\left(x^{3}\cos\frac{x}{2}+\frac12\right)\sqrt{4-x^{2}}\,dx.
\]

## Solution

The summand \(x^{3}\cos(x/2)\sqrt{4-x^{2}}\) is odd on \([-2,2]\), so its integral is 0. The remaining term is
\[
\frac12\int_{-2}^{2}\sqrt{4-x^{2}}\,dx=\int_{0}^{2}\sqrt{4-x^{2}}\,dx,
\]
a quarter disk of radius 2.

## Final answer

\[
\pi.
\]

Stored `answer_sympy`: `pi`.

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(4 - x**2)*(x**3*cos(x/2) + 1/2)` against `pi` (definite). The check is an exact closed evaluation. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
