# YANG-1.12-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 04, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-1}^{1} |x-|x-|x|||\,dx.
\]

## Solution

For \(x\ge 0\) the expression collapses to \(x\). For \(x<0\) it collapses to \(-3x\). Integrating those affine pieces on \([-1,0]\) and \([0,1]\) gives \(2\).

## Final answer

\[
2.
\]

## SymPy self-check

`verify/pack_gate.py` proves `Abs(x - Abs(x - Abs(x)))` against `2` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
