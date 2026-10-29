# YANG-1.12-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 05, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-2\pi}^{2\pi} |\sin x|\,dx.
\]

## Solution

The minimum of \(\sin\) on \([0,\pi]\) is \(0\), so \(|\sin t|=\sin t\) there. Each interval \([k\pi,(k+1)\pi]\) for \(k=-2,-1,0,1\) shifts onto that interval, and \(\int_{k\pi}^{(k+1)\pi}|\sin x|\,dx=2\). Four intervals give \(8\). The ordinary integrator's value \(4\) on these endpoints is rejected.

## Final answer

\[
8.
\]

## SymPy self-check

`verify/pack_gate.py` proves `Abs(sin(x))` against `8` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
