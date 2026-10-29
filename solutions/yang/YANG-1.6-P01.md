# YANG-1.6-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 1, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int x^{2} e^{x}\,dx.
\]

## Solution

Integrate by parts twice with the polynomial factor differentiated. The first step gives \(x^{2}e^{x}-2\int x e^{x}\,dx\). The second gives \(x^{2}e^{x}-2xe^{x}+2\int e^{x}\,dx\).

## Final answer

\[
e^{x}(x^{2}-2x+2).
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `x**2*exp(x)`. The stored answer is `x**2*exp(x) - 2*x*exp(x) + 2*exp(x)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
