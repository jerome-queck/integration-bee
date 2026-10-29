# YANG-3.8-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 13, printed p. 68 (PDF p. 69).

## Problem

∫_0^9 e sqrt(1+sqrt(x)) dx

\[
e \sqrt{\sqrt{x} + 1}
\]

## Solution

Put \(u=\sqrt{x}\) and then \(w=1+u\). The integral is
\[
2e\int_1^4(w^{3/2}-w^{1/2})\,dw=2e\Bigl[\frac25 w^{5/2}-\frac23 w^{3/2}\Bigr]_1^4=\frac{232e}{15}.
\]

## Final answer

\[
\frac{232 e}{15}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `E*sqrt(sqrt(x) + 1)`, `answer_sympy` is `232*E/15`, and `limits` is `['0', '9']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
