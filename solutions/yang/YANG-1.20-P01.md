# YANG-1.20-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 01, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{\infty} \frac{\ln(\sqrt{x}+1)}{x\sqrt{x}}\,dx.
\]

## Solution

The substitution \(x=t^{2}\) gives \(2\int_{0}^{\infty}\ln(1+t)/t^{2}\,dt\). An antiderivative is \(2(-\ln(1+t)/t+\ln t-\ln(1+t))\). It tends to \(0\) at infinity and to \(-\infty\) at \(0\), so the improper integral diverges to \(+\infty\).

## Final answer

\[
\infty.
\]

## SymPy self-check

`verify/pack_gate.py` proves `log(sqrt(x) + 1)/x**(3/2)` against `oo` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
