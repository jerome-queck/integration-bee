# YANG-1.20-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 07, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{1} \frac{\ln(1+x+x^{2})}{x}\,dx.
\]

## Solution

On \((0,1)\), \(1+x+x^{2}=(1-x^{3})/(1-x)\), so the integrand is \((\ln(1-x^{3})-\ln(1-x))/x\). The two improper integrals are \(-\pi^{2}/18\) and \(-\pi^{2}/6\), and their difference is \(\pi^{2}/9\).

## Final answer

\[
\frac{\pi^{2}}{9}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `log(x**2 + x + 1)/x` against `pi**2/9` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
