# YANG-1.12-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 07, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-\infty}^{\infty} e^{-|x|}\,dx.
\]

## Solution

The integrand is even. On \([0,\infty)\) it is \(e^{-x}\), and twice that improper integral is \(2\).

## Final answer

\[
2.
\]

## SymPy self-check

`verify/pack_gate.py` proves `exp(-Abs(x))` against `2` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
