# YANG-1.6-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 9, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \frac{\ln x}{x^{2}}\,dx.
\]

## Solution

Differentiate \(\ln x\) and integrate \(x^{-2}\). The boundary term is \(-\ln x/x\), and \(-\int -x^{-2}\,dx\) supplies \(-1/x\).

## Final answer

\[
-\frac{\ln x}{x}-\frac{1}{x}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `log(x)/x**2`. The stored answer is `-log(x)/x - 1/x`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
