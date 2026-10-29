# YANG-1.15-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 03, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \sec^{6} x\,dx.
\]

## Solution

\(\sec^{6} x=(1+\tan^{2} x)^{2}\sec^{2} x\). The substitution \(u=\tan x\) integrates to \(\tan x+\tfrac23\tan^{3} x+\tfrac15\tan^{5} x\). Differentiation recovers the integrand.

## Final answer

\[
\frac{\tan^{5}{\left(x \right)}}{5} + \frac{2 \tan^{3}{\left(x \right)}}{3} + \tan{\left(x \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sec(x)**6` against `tan(x)**5/5 + 2*tan(x)**3/3 + tan(x)` (indefinite). The check differentiates the stored antiderivative.
