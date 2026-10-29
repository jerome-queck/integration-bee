# YANG-1.7-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.7 Basic Trig-Substitution, practice item 7, printed p. 14 (PDF p. 15).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=15).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \frac{\sqrt{1-x^{2}}}{x^{2}}\,dx.
\]

## Solution

With \(x=\sin\theta\), the integrand becomes \(\cot^{2}\theta=\csc^{2}\theta-1\). Integrating gives \(-\cot\theta-\theta\).

## Final answer

\[
-\frac{\sqrt{1-x^{2}}}{x}-\arcsin x.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `sqrt(1 - x**2)/x**2`. The stored answer is `-asin(x) - sqrt(1 - x**2)/x`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
