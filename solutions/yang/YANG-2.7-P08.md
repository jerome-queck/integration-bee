# YANG-2.7-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 8, printed p. 46 (PDF p. 47).

## Problem

∫_0^{∞} atan(x)/((sqrt(1+x^2)+x) sqrt(1+x^2)) dx

\[
\frac{\operatorname{atan}{\left(x \right)}}{\left(x + \sqrt{x^{2} + 1}\right) \sqrt{x^{2} + 1}}
\]

## Solution

Put \(x=\sinh u\), \(u\ge 0\). Then \(\sqrt{1+\sinh^2 u}=\cosh u\) and \(\cosh u+\sinh u=e^u\), so the integrand becomes \(e^{-u}\operatorname{atan}(\sinh u)\). Differentiating \(-e^{-u}\operatorname{atan}(\sinh u)\) leaves the extra term \(e^{-u}/\cosh u\), and the boundary term vanishes at both ends. Rewriting the extra term in exponentials gives \(2e^{-2u}/(1+e^{-2u})\). The substitution \(t=e^{-2u}\) turns the integral into \(\int_0^1 dt/(1+t)=\log 2\).

## Final answer

\[
\log{\left(2 \right)}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `atan(x)/((x + sqrt(x**2 + 1))*sqrt(x**2 + 1))`, `answer_sympy` is `log(2)`, and `limits` is `['0', 'oo']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
