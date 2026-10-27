# YANG-1.3-Ex01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.3 Symmetry, Example 1, printed p. 9 (PDF p. 10).
- [Printed problem and worked answer](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=10).

## Status: resolved extraction error

The guide prints the fraction \(8/3\). The earlier text extraction stored only
its numerator, `8`, as the catalog answer. The catalog now stores `8/3`, the
printed integrand, and the limits \([-1,1]\), with `verify: sympy`. This corrects
the extraction; it does not change the guide's answer.

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

The catalog uses `sympy_expr=(x+1)*(x**2+1)`, `limits=["-1", "1"]`,
and `answer_sympy=8/3`. `verify/pack_gate.py` proves the row by exact polynomial
integration. The stale extracted answer `8` and the wrong answer `0` are
rejected by the same definite-answer comparison.
