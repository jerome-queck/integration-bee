# YANG-3.8-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 5, printed p. 68 (PDF p. 69).

## Problem

∫_{-∞}^{∞} dx/(x^2 + π x + π^2)

\[
\frac{1}{x^{2} + \pi x + \pi^{2}}
\]

## Solution

Complete the square: \(x^2+\pi x+\pi^2=(x+\pi/2)^2+3\pi^2/4\). The arctangent integral over the whole line is \(\pi/a\) with \(a=\pi\sqrt{3}/2\), which equals \(2/\sqrt{3}\).

## Final answer

\[
\frac{2 \sqrt{3}}{3}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `1/(x**2 + pi*x + pi**2)`, `answer_sympy` is `2*sqrt(3)/3`, and `limits` is `['-oo', 'oo']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
