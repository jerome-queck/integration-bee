# YANG-3.8-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 3, printed p. 68 (PDF p. 69).

## Problem

∫_0^{∞} exp(-x^2) (x+1)^3 dx

\[
\left(x + 1\right)^{3} e^{- x^{2}}
\]

## Solution

Expand \((x+1)^3=x^3+3x^2+3x+1\). The half-line Gaussian moments \(\int_0^\infty e^{-x^2}\,dx=\sqrt{\pi}/2\), \(\int_0^\infty x e^{-x^2}\,dx=1/2\), \(\int_0^\infty x^2 e^{-x^2}\,dx=\sqrt{\pi}/4\), and \(\int_0^\infty x^3 e^{-x^2}\,dx=1/2\) add to \(2+5\sqrt{\pi}/4\).

## Final answer

\[
2 + \frac{5 \sqrt{\pi}}{4}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `(x + 1)**3*exp(-x**2)`, `answer_sympy` is `2 + 5*sqrt(pi)/4`, and `limits` is `['0', 'oo']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
