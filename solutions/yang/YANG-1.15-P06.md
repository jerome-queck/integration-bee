# YANG-1.15-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 06, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int (\tan^{4} x+\tan^{6} x)\,dx.
\]

## Solution

Factor \(\tan^{4} x(1+\tan^{2} x)=\tan^{4} x\sec^{2} x\). The substitution \(u=\tan x\) gives \(\tan^{5} x/5\).

## Final answer

\[
\frac{\tan^{5}{\left(x \right)}}{5}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `tan(x)**6 + tan(x)**4` against `tan(x)**5/5` (indefinite). The check differentiates the stored antiderivative.
