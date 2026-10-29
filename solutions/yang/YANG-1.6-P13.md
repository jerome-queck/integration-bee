# YANG-1.6-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 13, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \sqrt{x}\,\ln x\,dx.
\]

## Solution

Differentiate \(\ln x\) and integrate \(x^{1/2}\). Then \(\frac{2}{3}x^{3/2}\ln x-\frac{2}{3}\int x^{1/2}\,dx\).

## Final answer

\[
\frac{2}{3}x^{3/2}\ln x-\frac{4}{9}x^{3/2}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `sqrt(x)*log(x)`. The stored answer is `2*x**(3/2)*log(x)/3 - 4*x**(3/2)/9`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
