# YANG-1.6-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 11, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int (x+1)^{2}\cos x\,dx.
\]

## Solution

Differentiate \((x+1)^{2}\) and integrate \(\cos x\), twice. The formula for \(\int t^{2}\cos t\,dt\) with \(t=x+1\) is the same expansion.

## Final answer

\[
(x+1)^{2}\sin x+2(x+1)\cos x-2\sin x.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `(x + 1)**2*cos(x)`. The stored answer is `x**2*sin(x) + 2*x*sin(x) + 2*x*cos(x) - sin(x) + 2*cos(x)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
