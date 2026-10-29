# YANG-1.6-P20

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 20, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \frac{\ln x}{\sqrt{x}}\,dx.
\]

## Solution

Differentiate \(\ln x\) and integrate \(x^{-1/2}\). Then \(2\sqrt{x}\ln x-\int 2x^{-1/2}\,dx\).

## Final answer

\[
2\sqrt{x}\,\ln x-4\sqrt{x}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `log(x)/sqrt(x)`. The stored answer is `2*sqrt(x)*log(x) - 4*sqrt(x)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
