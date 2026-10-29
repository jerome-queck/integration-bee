# YANG-1.6-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 8, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int (x+e^{x})^{2}\,dx.
\]

## Solution

Expand \((x+e^{x})^{2}=x^{2}+2xe^{x}+e^{2x}\). Integrate the middle term by parts: \(\int xe^{x}\,dx=e^{x}(x-1)\).

## Final answer

\[
\frac{x^{3}}{3}+2e^{x}(x-1)+\frac{e^{2x}}{2}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `(x + exp(x))**2`. The stored answer is `x**3/3 + 2*x*exp(x) + exp(2*x)/2 - 2*exp(x)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
