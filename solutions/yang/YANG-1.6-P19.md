# YANG-1.6-P19

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 19, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \sqrt{e^{x}(x^{2}+6x+9)}\,dx.
\]

## Solution

The radicand is \(e^{x}(x+3)^{2}\). Because \(e^{x/2}>0\), \(\sqrt{e^{x}(x+3)^{2}}=e^{x/2}\sqrt{(x+3)^{2}}\). Set \(s=\sqrt{x^{2}+6x+9}\) and integrate \(e^{x/2}s\) by parts. The resulting quotient is \(2(x^{2}+4x+3)e^{x/2}/s\), which is \(2(x+1)e^{x/2}\) on \(x>-3\) and \(-2(x+1)e^{x/2}\) on \(x<-3\). Either one-sided expression misses the other side. The quotient matches the printed integrand on both.

## Final answer

\[
\frac{2(x^{2}+4x+3)e^{x/2}}{\sqrt{x^{2}+6x+9}}.
\]

## SymPy self-check

`verify/catalog_check.py` re-proves the stored row through `verify/pack_gate.py`. The stored integrand is `sqrt(x**2 + 6*x + 9)*exp(x/2)`. The stored answer is `2*x**2*exp(x/2)/sqrt(x**2 + 6*x + 9) + 8*x*exp(x/2)/sqrt(x**2 + 6*x + 9) + 6*exp(x/2)/sqrt(x**2 + 6*x + 9)`. SymPy simplifies the derivative of that answer minus the integrand to 0. The same call is an indefinite derivative check, not a numeric comparison.
