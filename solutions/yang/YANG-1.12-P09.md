# YANG-1.12-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 09, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{16} |\sqrt{x}-2|\,dx.
\]

## Solution

For nonnegative \(a,b\), \(a\le b\) exactly when \(a^{2}\le b^{2}\). Thus \(\sqrt{x}\le 2\) on \([0,4]\) and \(\sqrt{x}\ge 2\) on \([4,16]\). The antiderivatives \(\pm(\tfrac23 x^{3/2}-2x)\) add to \(16\).

## Final answer

\[
16.
\]

## SymPy self-check

`verify/pack_gate.py` proves `Abs(sqrt(x) - 2)` against `16` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
