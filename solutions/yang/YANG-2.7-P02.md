# YANG-2.7-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 2, printed p. 46 (PDF p. 47).

## Problem

∫_0^{1/2} x^2/(1-x^2)^{3/2} dx

\[
\frac{x^{2}}{\left(1 - x^{2}\right)^{\frac{3}{2}}}
\]

## Solution

Put \(x=\sin\theta\), so \(\theta\) runs from \(0\) to \(\pi/6\). The integral becomes \(\int_0^{\pi/6}\tan^2\theta\,d\theta=\int_0^{\pi/6}(\sec^2\theta-1)\,d\theta=\tan\theta-\theta\) evaluated on that interval, which is \(1/\sqrt{3}-\pi/6\).

## Final answer

\[
- \frac{\pi}{6} + \frac{\sqrt{3}}{3}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `x**2/(1 - x**2)**(3/2)`, `answer_sympy` is `-pi/6 + sqrt(3)/3`, and `limits` is `['0', '1/2']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
