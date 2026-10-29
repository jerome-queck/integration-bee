# YANG-1.15-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 08, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \sqrt{1+\cos x}\,dx.
\]

## Solution

The half-angle identity gives \(\sqrt{1+\cos x}=\sqrt{2}\,|\cos(x/2)|\). The antiderivative \(2\sqrt{2}\sin(x/2)\) has derivative \(\sqrt{2}\cos(x/2)\). The squares agree, and both sides agree at \(x=0\), which is the radical-branch check.

## Final answer

\[
2 \sqrt{2} \sin{\left(\frac{x}{2} \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(cos(x) + 1)` against `2*sqrt(2)*sin(x/2)` (indefinite). The check differentiates the stored antiderivative.
