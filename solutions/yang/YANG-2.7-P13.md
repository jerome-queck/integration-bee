# YANG-2.7-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 13, printed p. 46 (PDF p. 47).

## Problem

∫_0^1 dx/((1+x^2) sqrt(1-x^2))

\[
\frac{1}{\sqrt{1 - x^{2}} \left(x^{2} + 1\right)}
\]

## Solution

The antiderivative \(\operatorname{atan}(\sqrt{2}\,x/\sqrt{1-x^2})/\sqrt{2}\) differentiates back to the integrand. Its value at \(0\) is \(0\). The two-sided limit at \(1\) is the negative of the left-hand limit, and the left-hand limit is \(\sqrt{2}\,\pi/4=\pi/(2\sqrt{2})\).

## Final answer

\[
\frac{\sqrt{2} \pi}{4}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `1/(sqrt(1 - x**2)*(x**2 + 1))`, `answer_sympy` is `sqrt(2)*pi/4`, and `limits` is `['0', '1']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
