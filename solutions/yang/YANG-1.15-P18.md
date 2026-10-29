# YANG-1.15-P18

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 18, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \tan^{3} x\,dx.
\]

## Solution

\(\tan^{3} x=\sec^{2} x\tan x-\tan x\). Integrating gives \(\tfrac12\tan^{2} x+\ln(\cos x)\).

## Final answer

\[
\log{\left(\cos{\left(x \right)} \right)} + \frac{\tan^{2}{\left(x \right)}}{2}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `tan(x)**3` against `log(cos(x)) + tan(x)**2/2` (indefinite). The check differentiates the stored antiderivative.
