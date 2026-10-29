# YANG-1.15-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 07, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{1}{1+\sin x}\,dx.
\]

## Solution

Multiply by \(1-\sin x\). The numerator becomes \(\cos^{2} x\), so the integrand is \(\sec^{2} x-\sec x\tan x\), whose antiderivative is \(\tan x-\sec x\).

## Final answer

\[
\tan{\left(x \right)} - \sec{\left(x \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `1/(sin(x) + 1)` against `tan(x) - sec(x)` (indefinite). The check differentiates the stored antiderivative.
