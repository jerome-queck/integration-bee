# YANG-1.6-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 15, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \arcsin x\,dx.
\]

## Solution

Differentiate \(\arcsin x\) and integrate \(1\). Then \(\int x/\sqrt{1-x^{2}}\,dx=-\sqrt{1-x^{2}}\).

## Final answer

\[
x\arcsin x+\sqrt{1-x^{2}}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `asin(x)`. The stored answer is `x*asin(x) + sqrt(1 - x**2)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
