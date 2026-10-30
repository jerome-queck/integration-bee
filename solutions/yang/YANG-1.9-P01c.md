# YANG-1.9-P01c

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.9 Area of a Partial Circle, Hybrid Example, printed p. 17 (PDF p. 18).
- Printed answer: \(3\pi/2\).
- Worked source: the guide prints this final. The gate re-proves it.

## Problem

\[
\int_{-1}^{1} \frac{2-x^{2}}{\sqrt{1-x^{2}}}(1+x^{3})\,dx.
\]

## Solution

The algebraic identity
\[
\frac{2-x^{2}}{\sqrt{1-x^{2}}}=\frac{1}{\sqrt{1-x^{2}}}+\sqrt{1-x^{2}}
\]
splits the integrand into an even factor times \(1+x^{3}\). On \([-1,1]\) the \(x^{3}\) term is odd, so it contributes nothing. The two even integrals are \(\pi\) and \(\pi/2\).

## Final answer

\[
\frac{3\pi}{2}.
\]

Stored `answer_sympy`: `3*pi/2`.

## SymPy self-check

`verify/pack_gate.py` proves `(2 - x**2)*(x**3 + 1)/sqrt(1 - x**2)` against `3*pi/2` (definite). The check is an exact closed evaluation. Numeric agreement is not the proof.

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each indefinite antiderivative is differentiated, and each definite intermediate is an exact identity.
