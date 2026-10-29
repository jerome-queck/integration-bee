# YANG-1.9-P01b

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.9 Area of a Partial Circle, Exponential Example, printed p. 17 (PDF p. 18).
- Printed answer: \(\pi/4\).
- Worked source: the guide prints this final. The gate re-proves it.

## Problem

\[
\int_{0}^{\infty} \sqrt{e^{-2x}-e^{-4x}}\,dx.
\]

## Solution

Factor \(e^{-2x}\) out of the radical: \(\sqrt{e^{-2x}-e^{-4x}}=e^{-x}\sqrt{1-e^{-2x}}\). The substitution \(u=e^{-x}\) carries \([0,\infty)\) to \((0,1]\) and the integral to \(\int_{0}^{1}\sqrt{1-u^{2}}\,du\), a quarter disk of radius 1.

## Final answer

\[
\frac{\pi}{4}.
\]

Stored `answer_sympy`: `pi/4`.

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(exp(-2*x) - exp(-4*x))` against `pi/4` (definite). The check is an exact closed evaluation. Numeric agreement is not the proof.
