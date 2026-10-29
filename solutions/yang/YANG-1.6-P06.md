# YANG-1.6-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 6, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int x\ln x\,dx.
\]

## Solution

Differentiate \(\ln x\) and integrate \(x\). Then \(\frac{x^{2}}{2}\ln x-\int\frac{x}{2}\,dx\).

## Final answer

\[
\frac{x^{2}}{2}\ln x-\frac{x^{2}}{4}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `x*log(x)`. The stored answer is `x**2*log(x)/2 - x**2/4`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
