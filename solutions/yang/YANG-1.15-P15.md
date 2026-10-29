# YANG-1.15-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 15, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{\cos^{2} x}{2\cos^{2} x-1}\,dx.
\]

## Solution

The denominator is \(\cos 2x\), and the quotient simplifies to \(\tfrac12+\tfrac12\sec 2x\). Integrating gives \(\tfrac12 x+\tfrac14\ln|\sec 2x+\tan 2x|\).

## Final answer

\[
\frac{x}{2} + \frac{\log{\left(\tan{\left(2 x \right)} + \sec{\left(2 x \right)} \right)}}{4}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `cos(x)**2/(2*cos(x)**2 - 1)` against `x/2 + log(tan(2*x) + sec(2*x))/4` (indefinite). The check differentiates the stored antiderivative.
