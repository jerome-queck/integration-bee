# YANG-2.7-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 11, printed p. 46 (PDF p. 47).

## Problem

∫_0^1 dx/((1+sqrt(x)) sqrt(x-x^2))

\[
\frac{1}{\left(\sqrt{x} + 1\right) \sqrt{- x^{2} + x}}
\]

## Solution

For \(x>0\), \(F(x)=2(\sqrt{x}-1)/\sqrt{1-x}\) differentiates back to the integrand. The right-hand limit at \(1\) is \(0\) and \(F(0)=-2\), so the definite value is \(2\).

## Final answer

\[
2
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `1/((sqrt(x) + 1)*sqrt(-x**2 + x))`, `answer_sympy` is `2`, and `limits` is `['0', '1']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
