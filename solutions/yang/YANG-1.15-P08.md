# YANG-1.15-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 08, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \sqrt{1+\cos x}\,dx.
\]

## Solution

The half-angle identity gives \(\sqrt{1+\cos x}=\sqrt{2}\,|\cos(x/2)|\). The catalog antiderivative is \(2\sin x/\sqrt{1+\cos x}\), which equals \(2\sqrt{2}\sin(x/2)\operatorname{sign}(\cos(x/2))\) between the odd multiples of \(\pi\). That expression jumps by \(-4\sqrt{2}\) at each odd multiple of \(\pi\). The local formula \(2\sqrt{2}\sin(x/2)\) matches only where \(\cos(x/2)\ge 0\).

## Final answer

\[
\frac{2\sin x}{\sqrt{1+\cos x}}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(cos(x) + 1)` against `2*sin(x)/sqrt(cos(x) + 1)` (indefinite). The check differentiates the stored antiderivative.
