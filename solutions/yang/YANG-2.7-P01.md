# YANG-2.7-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 1, printed p. 46 (PDF p. 47).

## Problem

∫ x/((1-x) sqrt(1-x^2)) dx

\[
\frac{x}{\left(1 - x\right) \sqrt{1 - x^{2}}}
\]

## Solution

Put \(x=\sin\theta\), with \(\cos\theta>0\) on the interval where \(|x|<1\). The integral becomes
\[
\int\frac{\sin\theta}{1-\sin\theta}\,d\theta=\int\Bigl(-1+\frac{1+\sin\theta}{\cos^2\theta}\Bigr)d\theta=\int(-1+\sec^2\theta+\sec\theta\tan\theta)\,d\theta.
\]
An antiderivative is \(-\theta+\tan\theta+\sec\theta\), which is
\[
\frac{x}{\sqrt{1-x^2}}+\frac{1}{\sqrt{1-x^2}}-\operatorname{asin}(x).
\]
Differentiating that expression returns the integrand.

## Final answer

\[
\frac{x}{\sqrt{1 - x^{2}}} - \operatorname{asin}{\left(x \right)} + \frac{1}{\sqrt{1 - x^{2}}}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `x/((1 - x)*sqrt(1 - x**2))`, `answer_sympy` is `x/sqrt(1 - x**2) - asin(x) + 1/sqrt(1 - x**2)`, and `limits` is `[]`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
