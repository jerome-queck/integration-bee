# YANG-1.7-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.7 Basic Trig-Substitution, practice item 4, printed p. 14 (PDF p. 15).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=15).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \frac{dx}{(1+x^{2})^{3/2}}.
\]

## Solution

With \(x=\tan\theta\), the integrand becomes \(\cos\theta\), whose integral is \(\sin\theta=x/\sqrt{1+x^{2}}\).

## Final answer

\[
\frac{x}{\sqrt{1+x^{2}}}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `(x**2 + 1)**(-3/2)`. The stored answer is `x/sqrt(x**2 + 1)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
