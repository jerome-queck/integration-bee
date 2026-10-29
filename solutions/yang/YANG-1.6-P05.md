# YANG-1.6-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 5, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int x\sec^{2}x\,dx.
\]

## Solution

Integrate \(\sec^{2}x\) and differentiate \(x\). The new integral is \(\int\tan x\,dx=-\ln(\cos x)\).

## Final answer

\[
x\tan x+\ln(\cos x).
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `x*sec(x)**2`. The stored answer is `x*tan(x) + log(cos(x))`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
