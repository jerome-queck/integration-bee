# YANG-3.8-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 2, printed p. 68 (PDF p. 69).

## Problem

∫_{-1}^{1} 15 (1 + real_cbrt(x))^3 dx

\[
15 \left(\sqrt[3]{\left|{x}\right|} \operatorname{sign}{\left(x \right)} + 1\right)^{3}
\]

## Solution

Let \(u\) be the real cube root of \(x\), so \(x=u^3\) and \(dx=3u^2\,du\), with \(u\) running from \(-1\) to \(1\). The integral becomes \(\int_{-1}^1 15(1+u)^3\cdot 3u^2\,du\), a polynomial integral equal to \(84\). The complex principal cube root is a different integrand on the negative half of the interval.

## Final answer

\[
84
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `15*(Abs(x)**(1/3)*sign(x) + 1)**3`, `answer_sympy` is `84`, and `limits` is `['-1', '1']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
