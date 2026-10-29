# YANG-2.7-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 4, printed p. 46 (PDF p. 47).

## Problem

∫_0^1 atan(x/sqrt(1-x^2)) dx

\[
\operatorname{atan}{\left(\frac{x}{\sqrt{1 - x^{2}}} \right)}
\]

## Solution

Put \(x=\sin\theta\), so \(\theta\) runs from \(0\) to \(\pi/2\). Then \(\operatorname{atan}(x/\sqrt{1-x^2})=\theta\) on \([0,\pi/2)\), and the integral is \(\int_0^{\pi/2}\theta\cos\theta\,d\theta=\pi/2-1\).

## Final answer

\[
-1 + \frac{\pi}{2}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `atan(x/sqrt(1 - x**2))`, `answer_sympy` is `-1 + pi/2`, and `limits` is `['0', '1']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
