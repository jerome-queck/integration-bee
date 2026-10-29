# YANG-1.15-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 14, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{1}{(\sec x-\tan x)^{2}}\,dx.
\]

## Solution

\(\sec^{2} x-\tan^{2} x=1\), so \(1/(\sec x-\tan x)=\sec x+\tan x\) and the integrand is \((\sec x+\tan x)^{2}=2\sec^{2} x+2\sec x\tan x-1\). The antiderivative is \(-x+2\sec x+2\tan x\).

## Final answer

\[
- x + 2 \tan{\left(x \right)} + 2 \sec{\left(x \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `(-tan(x) + sec(x))**(-2)` against `-x + 2*tan(x) + 2*sec(x)` (indefinite). The check differentiates the stored antiderivative.
