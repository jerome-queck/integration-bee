# YANG-2.7-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 6, printed p. 46 (PDF p. 47).

## Problem

∫_0^1 (1-x)/(asin(x) sqrt(1-x^2)+1-x^2) dx

\[
\frac{1 - x}{- x^{2} + \sqrt{1 - x^{2}} \operatorname{asin}{\left(x \right)} + 1}
\]

## Solution

The denominator factors as \(\sqrt{1-x^2}(\operatorname{asin}(x)+\sqrt{1-x^2})\). The antiderivative \(\log(\operatorname{asin}(x)+\sqrt{1-x^2})\) differentiates back to the integrand. Its values at the endpoints differ by \(\log(\pi/2)\).

## Final answer

\[
- \log{\left(2 \right)} + \log{\left(\pi \right)}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `(1 - x)/(-x**2 + sqrt(1 - x**2)*asin(x) + 1)`, `answer_sympy` is `-log(2) + log(pi)`, and `limits` is `['0', '1']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
