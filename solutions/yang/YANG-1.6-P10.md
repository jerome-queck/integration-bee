# YANG-1.6-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 10, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \sin x\,\ln(\sec x)\,dx.
\]

## Solution

Set \(u=\cos x\), so \(\sin x\,dx=-du\) and \(\ln(\sec x)=-\ln u\). The integral becomes \(\int\ln u\,du=u\ln u-u\), which returns to \(x\) as \(-\cos x\ln(\sec x)-\cos x\).

## Final answer

\[
-\cos x\,\ln(\sec x)-\cos x.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `log(sec(x))*sin(x)`. The stored answer is `-log(sec(x))*cos(x) - cos(x)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
