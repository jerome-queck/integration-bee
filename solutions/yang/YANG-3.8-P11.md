# YANG-3.8-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 11, printed p. 68 (PDF p. 69).

## Problem

∫_0^{∞} dx/(e^x + e^{-(x+1)})

\[
\frac{1}{e^{x} + e^{- x - 1}}
\]

## Solution

The antiderivative \(\sqrt{e}\,\operatorname{atan}(e^x\sqrt{e})\) differentiates back to the integrand. At \(0\) it is \(\sqrt{e}\,\operatorname{atan}(\sqrt{e})\), and as \(x\to\infty\) it tends to \(\sqrt{e}\,\pi/2\). The difference is \(\sqrt{e}(\pi/2-\operatorname{atan}(\sqrt{e}))\).

## Final answer

\[
- e^{\frac{1}{2}} \operatorname{atan}{\left(e^{\frac{1}{2}} \right)} + \frac{\pi e^{\frac{1}{2}}}{2}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `1/(exp(x) + exp(-x - 1))`, `answer_sympy` is `-exp(1/2)*atan(exp(1/2)) + pi*exp(1/2)/2`, and `limits` is `['0', 'oo']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
