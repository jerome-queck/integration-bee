# YANG-1.9-P01a

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.9 Area of a Partial Circle, Substitution Example, printed p. 17 (PDF p. 18).
- Printed answer: \(9\pi/4\).
- Worked source: the guide prints this final. The gate re-proves it.

## Problem

\[
\int_{0}^{3} \sqrt{6x-x^{2}}\,dx.
\]

## Solution

Complete the square: \(6x-x^{2}=9-(x-3)^{2}\). The shift \(u=x-3\) carries \([0,3]\) to \([-3,0]\). The integrand becomes \(\sqrt{9-u^{2}}\), and the integral is a quarter disk of radius 3.

## Final answer

\[
\frac{9\pi}{4}.
\]

Stored `answer_sympy`: `9*pi/4`.

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(-x**2 + 6*x)` against `9*pi/4` (definite). The check is an exact closed evaluation. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
