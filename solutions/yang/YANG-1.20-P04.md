# YANG-1.20-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 04, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{\infty} \frac{\ln x\,(\ln x+1)}{x^{2x-1}}\,dx.
\]

## Solution

SymPy evaluates the improper integral in closed form as \(1/4\). The same value is the integral \(\int_{1}^{\infty}\ln u/u^{3}\,du\) obtained by tracking \(u=x^{x}\) down to its minimum at \(x=1/e\) and back up to infinity.

## Final answer

\[
\frac{1}{4}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `x**(1 - 2*x)*(log(x) + 1)*log(x)` against `1/4` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
