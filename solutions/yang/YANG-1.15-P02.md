# YANG-1.15-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 02, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{\pi/2} (1+\cos x)^{2}\,dx.
\]

## Solution

Expand as \(1+2\cos x+\cos^{2} x\) and write \(\cos^{2} x=(1+\cos 2x)/2\). The definite integral is \(2+3\pi/4\).

## Final answer

\[
2 + \frac{3 \pi}{4}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `(cos(x) + 1)**2` against `2 + 3*pi/4` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
