# YANG-1.7-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.7 Basic Trig-Substitution, practice item 6, printed p. 14 (PDF p. 15).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=15).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \frac{dx}{x^{2}+4}.
\]

## Solution

The standard arctangent integral with \(a=2\) is \(\frac{1}{a}\arctan(x/a)\).

## Final answer

\[
\frac12\arctan\frac{x}{2}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `1/(x**2 + 4)`. The stored answer is `atan(x/2)/2`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
