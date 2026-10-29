# YANG-3.8-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 1, printed p. 68 (PDF p. 69).
- The radical bar covers the fraction. The exponent is \(\sqrt{e^{\sqrt{x}}}+\sqrt{x}\).

## Problem

∫ from 0 to \((\ln 4)^2\) of \(\sqrt{\exp(\sqrt{x}+\sqrt{\exp(\sqrt{x})})/x}\,dx\)

\[
\sqrt{\frac{e^{\sqrt{x} + \sqrt{e^{\sqrt{x}}}}}{x}}
\]

## Solution

Set \(t=\sqrt{x}\). The limits run from 0 to \(\ln 4\), and the integral becomes

\[
2\int_0^{\ln 4}\exp(t/2)\exp(e^{t/2}/2)\,dt.
\]

Set \(u=e^{t/2}\). Then \(u\) runs from 1 to 2 and \(dt=2\,du/u\), so the integral is \(4\int_1^2 e^{u/2}\,du=8(e-\sqrt{e})\).

## Final answer

\[
- 8 e^{\frac{1}{2}} + 8 e
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `sqrt(exp(sqrt(x) + sqrt(exp(sqrt(x))))/x)`, `answer_sympy` is `-8*exp(1/2) + 8*E`, and `limits` is `['0', 'log(4)**2']`. `verify/yang_l8.py` checks the two substitutions before the elementary integral.
