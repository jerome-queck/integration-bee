# YANG-1.3-Ex01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.3 Symmetry, Example 1
- The catalog row stays `verify: manual`. The text extract stores the numerator `8` on its own line. The guide prints the fraction \(8/3\).

## Problem

\[
\int_{-1}^{1}(x+1)(x^2+1)\,dx.
\]

## Solution

Expand the integrand as \(x^3+x^2+x+1\). The powers \(x^3\) and \(x\) are odd, so their integrals on \([-1,1]\) vanish. The even part contributes

\[
2\int_0^1(x^2+1)\,dx=2\Bigl[\frac{x^3}{3}+x\Bigr]_0^1=2\Bigl(\frac13+1\Bigr)=\frac83.
\]

This is the evaluation printed under Example 1.

## Final answer

\[
\frac83.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_yang_1_3_ex01`. SymPy integrates \((x+1)(x^2+1)\) from \(-1\) to \(1\) and gets \(8/3\). The same call on the even reduction \(2\int_0^1(x^2+1)\,dx\) returns \(8/3\).
