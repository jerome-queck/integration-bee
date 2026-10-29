# YANG-3.8-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 4, printed p. 68 (PDF p. 69).

## Problem

∫_1^{∞} dx/(x (x^{ln 4}+1))

\[
\frac{1}{x \left(x^{\log{\left(4 \right)}} + 1\right)}
\]

## Solution

Put \(u=\log x\), so the integral is \(\int_0^\infty du/(4^u+1)\). With \(t=e^{-u\log 4}\), this is \(\log 2/\log 4=1/2\).

## Final answer

\[
\frac{1}{2}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `1/(x*(x**log(4) + 1))`, `answer_sympy` is `1/2`, and `limits` is `['1', 'oo']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
