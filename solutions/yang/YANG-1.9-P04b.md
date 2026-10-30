# YANG-1.9-P04b

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.9 Area of a Partial Circle, Ellipse Example, printed p. 16 (PDF p. 17).
- Printed answer: \(\sqrt{3}\,\pi\).
- Worked source: the guide prints this final. The gate re-proves it.

## Problem

\[
\int_{0}^{2}\sqrt{12-3x^{2}}\,dx.
\]

## Solution

Factor the radicand: \(\sqrt{12-3x^{2}}=\sqrt{3}\,\sqrt{4-x^{2}}\). The guide prints that rewrite and boxes \(\sqrt{3}\,\pi\). The integral of \(\sqrt{4-x^{2}}\) from 0 to 2 is a quarter disk of radius 2, with area \(\pi\), so the factor \(\sqrt{3}\) produces \(\sqrt{3}\,\pi\). The text layer had glued the printed page number 16 onto this final. The page image shows the boxed value \(\sqrt{3}\,\pi\).

The rewrite is the last display of this example. It is not a second problem.

## Final answer

\[
\sqrt{3}\,\pi.
\]

Stored `answer_sympy`: `sqrt(3)*pi`.

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(12 - 3*x**2)` against `sqrt(3)*pi` (definite). The check is an exact closed evaluation. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
