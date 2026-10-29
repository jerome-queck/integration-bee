# YANG-1.20-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 02, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-1}^{\infty} e^{-x^{2}}(5x^{4}-2x^{6})\,dx.
\]

## Solution

The integrand is the derivative of \(x^{5}e^{-x^{2}}\). The primitive tends to \(0\) at infinity and equals \(-e^{-1}\) at \(-1\), so the improper integral is \(e^{-1}\).

## Final answer

\[
e^{-1}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `(-2*x**6 + 5*x**4)*exp(-x**2)` against `exp(-1)` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
