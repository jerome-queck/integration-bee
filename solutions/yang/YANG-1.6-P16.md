# YANG-1.6-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 16, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int x\sec^{2}x\tan x\,dx.
\]

## Solution

The substitution \(u=\sec x\) gives \(\int\sec^{2}x\tan x\,dx=\sec^{2}x/2\). Parts with that antiderivative leaves \(\frac12\int\sec^{2}x\,dx\).

## Final answer

\[
\frac{x}{2}\sec^{2}x-\frac12\tan x.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `x*tan(x)*sec(x)**2`. The stored answer is `x*sec(x)**2/2 - tan(x)/2`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
