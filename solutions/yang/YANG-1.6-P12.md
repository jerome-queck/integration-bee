# YANG-1.6-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 12, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \arctan x\,dx.
\]

## Solution

Differentiate \(\arctan x\) and integrate \(1\). The new integral is \(\int x/(1+x^{2})\,dx=\frac12\ln(1+x^{2})\).

## Final answer

\[
x\arctan x-\frac12\ln(x^{2}+1).
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `atan(x)`. The stored answer is `x*atan(x) - log(x**2 + 1)/2`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
