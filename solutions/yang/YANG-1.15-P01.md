# YANG-1.15-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 01, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{\pi/2} \sin^{2} x\,dx.
\]

## Solution

\(\sin^{2} x=(1-\cos 2x)/2\). Integrating from \(0\) to \(\pi/2\) leaves \(\pi/4\).

## Final answer

\[
\frac{\pi}{4}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sin(x)**2` against `pi/4` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
