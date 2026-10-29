# YANG-1.12-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 02, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{5} \frac{1}{x+|x-1|}\,dx.
\]

## Solution

On \([0,1]\) the denominator is \(1\). On \([1,5]\) it is \(2x-1\), whose integral is \(\tfrac12\ln 9\). The sum is \(1+\tfrac12\ln 9\).

## Final answer

\[
1 + \log{\left(3 \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `1/(x + Abs(x - 1))` against `1 + log(3)` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
