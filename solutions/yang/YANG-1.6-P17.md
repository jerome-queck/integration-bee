# YANG-1.6-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 17, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int x\,2^{x}\,dx.
\]

## Solution

The raised glyph is the exponent on \(2\), so the integrand is \(x\,2^{x}=x e^{x\ln 2}\). Parts, or the formula for \(\int x e^{ax}\,dx\), gives \(2^{x}(x/\ln 2-1/(\ln 2)^{2})\).

## Final answer

\[
2^{x}\left(\frac{x}{\ln 2}-\frac{1}{(\ln 2)^{2}}\right).
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `2**x*x`. The stored answer is `2**x*x/log(2) - 2**x/log(2)**2`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
