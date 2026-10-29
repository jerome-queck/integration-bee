# YANG-6.1-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §6.1 Inverse Jailbreaking, Beginner Example, printed p. 92 (PDF p. 93).

## Problem

∫_1^2 acsc(sqrt(x)) dx

\[
\operatorname{acsc}{\left(\sqrt{x} \right)}
\]

## Solution

If \(y=\operatorname{acsc}(\sqrt{x})\), then \(x=\csc^2 y\). The inverse-function formula with limits from \(\operatorname{acsc}(1)=\pi/2\) to \(\operatorname{acsc}(\sqrt{2})=\pi/4\) gives
\[
2\cdot\frac{\pi}{4}-1\cdot\frac{\pi}{2}-\int_{\pi/2}^{\pi/4}\csc^2 y\,dy=1,
\]
which is the evaluation printed in the beginner example.

## Final answer

\[
1
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `acsc(sqrt(x))`, `answer_sympy` is `1`, and `limits` is `['1', '2']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
