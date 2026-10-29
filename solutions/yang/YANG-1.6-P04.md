# YANG-1.6-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 4, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int x e^{-x}\,dx.
\]

## Solution

The printed fraction is \(x/e^{x}\). Differentiate \(x\) and integrate \(e^{-x}\). The boundary term is \(-xe^{-x}\), and the remaining integral is \(\int e^{-x}\,dx\).

## Final answer

\[
-e^{-x}(x+1).
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `x*exp(-x)`. The stored answer is `-x*exp(-x) - exp(-x)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
