# YANG-1.15-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 16, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{\tan x}{\tan 2x}\,dx.
\]

## Solution

The double-angle formula gives \(\tan x/\tan 2x=(1-\tan^{2} x)/2=1-\tfrac12\sec^{2} x\). The antiderivative is \(x-\tfrac12\tan x\).

## Final answer

\[
x - \frac{\tan{\left(x \right)}}{2}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `tan(x)/tan(2*x)` against `x - tan(x)/2` (indefinite). The check differentiates the stored antiderivative.
