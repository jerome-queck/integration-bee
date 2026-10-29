# YANG-2.4-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.4 Gamma Function Integral, practice item 12, printed p. 43 (PDF p. 44).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^{π/2} sec(x)^6 e^{-tan(x)} dx.

Catalog integrand `exp(-tan(x))*sec(x)**6`, limits `['0', 'pi/2']`, display `e^{- \tan{\left(x \right)}} \sec^{6}{\left(x \right)}`.

## Solution

On \([0,\pi/2)\), \(u=\tan x\) is a bijection onto \([0,\infty)\) and \(du=\sec^2 x\,dx\). The identity \(\sec^2 x=1+\tan^2 x\) gives \(\sec^6 x=(1+\tan^2 x)^2\sec^2 x\), so
\[
\int_0^{\pi/2}\sec^6 x\,e^{-\tan x}\,dx=\int_0^\infty(1+u^2)^2 e^{-u}\,du
=\int_0^\infty(1+2u^2+u^4)e^{-u}\,du=0!+2\cdot 2!+4!=1+4+24=29.
\]
`verify/yang_certificates.py` checks this substitution and evaluates the reduced Gamma integral. The ordinary definite integrator leaves the original integrand unevaluated, so the row uses that certificate.

## Final answer

The catalog stores `answer_sympy` as `29` and `answer_latex` as `29`.

## SymPy self-check

`verify/yang_certificates.py` evaluates the tangent substitution, and `verify/pack_gate.py` accepts that value. A wrong value such as 28 is rejected. `make check` re-proves the stored fields and does not open the PDF.
