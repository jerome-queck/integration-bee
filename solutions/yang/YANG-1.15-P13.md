# YANG-1.15-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 13, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{1}{\sin^{2} x\cos^{2} x}\,dx.
\]

## Solution

\(\sin^{2} x+\cos^{2} x=1\) splits the integrand into \(\sec^{2} x+\csc^{2} x\). The antiderivative is \(\tan x-\cot x\).

## Final answer

\[
\tan{\left(x \right)} - \cot{\left(x \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `1/(sin(x)**2*cos(x)**2)` against `tan(x) - cot(x)` (indefinite). The check differentiates the stored antiderivative.
