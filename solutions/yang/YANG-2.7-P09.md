# YANG-2.7-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 9, printed p. 46 (PDF p. 47).

## Problem

∫_1^{√2} exp(asec(x)) sqrt(x^2-1) dx

\[
\sqrt{x^{2} - 1} e^{\operatorname{asec}{\left(x \right)}}
\]

## Solution

On \(x>0\),
\[
F(x)=\frac12 e^{\operatorname{asec}(x)}\,x\bigl(\sqrt{x^2-1}-1\bigr)
\]
differentiates back to the integrand. The interval \([1,\sqrt{2}]\) lies in that half-line, and \(F(\sqrt{2})-F(1)=1/2\).

## Final answer

\[
\frac{1}{2}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `sqrt(x**2 - 1)*exp(asec(x))`, `answer_sympy` is `1/2`, and `limits` is `['1', 'sqrt(2)']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
