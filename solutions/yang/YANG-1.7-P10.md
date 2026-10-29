# YANG-1.7-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.7 Basic Trig-Substitution, practice item 10, printed p. 14 (PDF p. 15).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=15).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \frac{\sqrt{x^{2}-1}}{x}\,dx.
\]

## Solution

With \(x=\sec\theta\), the integral becomes \(\int\tan^{2}\theta\,d\theta=\tan\theta-\theta\). The same antiderivative is \(\sqrt{x^{2}-1}-\arctan\sqrt{x^{2}-1}\). Its derivative simplifies identically to the integrand. Replacing the arctangent by \(\operatorname{arcsec} x\) matches only for \(x>1\).

## Final answer

\[
\sqrt{x^{2}-1}-\arctan\sqrt{x^{2}-1}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `sqrt(x**2 - 1)/x`. The stored answer is `sqrt(x**2 - 1) - atan(sqrt(x**2 - 1))`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
