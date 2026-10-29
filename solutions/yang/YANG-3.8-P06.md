# YANG-3.8-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 6, printed p. 68 (PDF p. 69).
- The logarithm's radical covers \(x+1\).

## Problem

∫ from 0 to ∞ of \(\ln(\sqrt{x+1})/(x\sqrt{x})\,dx\)

\[
\frac{\log{\left(\sqrt{x + 1} \right)}}{x^{\frac{3}{2}}}
\]

## Solution

For \(x>0\), the denominator \(x\sqrt{x}\) is \(x^{3/2}\). Set \(t=\sqrt{x}\). The integral becomes

\[
\int_0^{\infty}\frac{\ln(1+t^2)}{t^2}\,dt.
\]

The derivative of \(-\ln(1+t^2)/t\) is \(\ln(1+t^2)/t^2-2/(1+t^2)\). Both endpoint limits of \(\ln(1+t^2)/t\) are 0, and \(\int_0^{\infty}2/(1+t^2)\,dt=\pi\).

## Final answer

\[
\pi
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `log(sqrt(x + 1))/x**(3/2)`, `answer_sympy` is `pi`, and `limits` is `['0', 'oo']`. `verify/yang_l8.py` checks the substitution and the integration by parts.
