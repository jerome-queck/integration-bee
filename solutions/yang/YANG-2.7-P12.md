# YANG-2.7-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 12, printed p. 46 (PDF p. 47).

## Problem

∫_1^4 atan(sqrt(sqrt(x)-1)) dx

\[
\operatorname{atan}{\left(\sqrt{\sqrt{x} - 1} \right)}
\]

## Solution

Put \(t=\sqrt{x}\), so \(t\) runs from \(1\) to \(2\) and \(dx=2t\,dt\). Then put \(u=\sqrt{t-1}\), so \(t=u^2+1\) and \(u\) runs from \(0\) to \(1\). The integral becomes
\[
4\int_0^1 u(u^2+1)\operatorname{atan}(u)\,du.
\]
That elementary integral equals \(\pi-4/3\), which is the value the gate stores for the original limits.

## Final answer

\[
- \frac{4}{3} + \pi
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `atan(sqrt(sqrt(x) - 1))`, `answer_sympy` is `-4/3 + pi`, and `limits` is `['1', '4']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
