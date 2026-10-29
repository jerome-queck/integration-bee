# YANG-1.12-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 03, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-1}^{1} |e^{x}-1|\,dx.
\]

## Solution

\(\int_{0}^{h} e^{t}\,dt=e^{h}-1\) and \(e^{t}>0\), so \(e^{x}-1\ge 0\) on \([0,1]\). The same integral of \(e^{-t}\) gives \(1-e^{-u}\ge 0\). The substitution \(u=-x\) turns the left half into \(\int_{0}^{1}(1-e^{-u})\,du\). The two antiderivatives add to \(e+e^{-1}-2\).

## Final answer

\[
-2 + e^{-1} + e.
\]

## SymPy self-check

`verify/pack_gate.py` proves `Abs(exp(x) - 1)` against `-2 + exp(-1) + E` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
