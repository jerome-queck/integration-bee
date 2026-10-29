# YANG-3.8-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 9, printed p. 68 (PDF p. 69).

## Problem

∫_1^4 asec(x^{1/4}) dx

\[
\operatorname{asec}{\left(\sqrt[4]{x} \right)}
\]

## Solution

Put \(t=x^{1/4}\), so \(t\) runs from \(1\) to \(\sqrt{2}\) and \(dx=4t^3\,dt\). Integration by parts on \(t^4\operatorname{asec}(t)\) produces the boundary value \(\pi\) and the remainder \(\int_1^{\sqrt{2}} t^3/\sqrt{t^2-1}\,dt\). Put \(t=\sec\theta\) on \((0,\pi/4)\), where \(\tan\theta>0\), so the remainder is \(\int_0^{\pi/4}\sec^4\theta\,d\theta=\int_0^1(1+w^2)\,dw=4/3\). The value is \(\pi-4/3\). The direct antiderivative of the singular \(t\)-integral is not used.

## Final answer

\[
- \frac{4}{3} + \pi
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `asec(x**(1/4))`, `answer_sympy` is `-4/3 + pi`, and `limits` is `['1', '4']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
