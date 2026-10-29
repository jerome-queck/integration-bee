# YANG-1.18-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.18 King's/Queen's Rule, practice item 02, printed p. 31 (PDF p. 32).
- Printed answer: the guide prints the final below. Worked source: derived in this note.

## Problem

\[
\int_{0}^{1} \frac{\ln(x+1)}{\ln(2+x-x^{2})}\,dx.
\]

## Solution

On \([0,1]\), \(2+x-x^{2}=(1+x)(2-x)\) with both factors positive, so the denominator is \(\ln(1+x)+\ln(2-x)\). The integrand and its reflection \(x\mapsto 1-x\) add to \(1\). The substitution preserves the integral, so twice the value is \(\int_{0}^{1} 1\,dx\) and the value is \(1/2\), as the guide prints.

## Final answer

\[
\frac{1}{2}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `log(x + 1)/log(-x**2 + x + 2)` against `1/2` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
