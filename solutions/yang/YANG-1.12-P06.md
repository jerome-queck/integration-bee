# YANG-1.12-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 06, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{4} \frac{|x-1|}{|x-2|+|x-3|}\,dx.
\]

## Solution

On each of \([0,1]\), \([1,2]\), \([2,3]\), and \([3,4]\) every absolute value is affine, because a degree-1 polynomial keeps the sign of its endpoints. The four rational pieces integrate to \(2+\tfrac94\ln 3-\tfrac34\ln 5\).

## Final answer

\[
- \frac{3 \log{\left(5 \right)}}{4} + 2 + \frac{9 \log{\left(3 \right)}}{4}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `Abs(x - 1)/(Abs(x - 3) + Abs(x - 2))` against `-3*log(5)/4 + 2 + 9*log(3)/4` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
