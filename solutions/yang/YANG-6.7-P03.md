# YANG-6.7-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §6.7 Feynman Technique, Beginner Feynman Example, printed p. 111 (PDF p. 112).

## Problem

∫_0^1 (x^{10}-1)/ln(x) dx

\[
\frac{x^{10} - 1}{\log{\left(x \right)}}
\]

## Solution

For \(n> -1\) set \(I(n)=\int_0^1(x^n-1)/\log x\,dx\). Differentiating under the integral sign gives \(I'(n)=\int_0^1 x^n\,dx=1/(n+1)\), so \(I(n)=\log(n+1)+C\). The integrand vanishes at \(n=0\), hence \(C=0\). The printed case is \(n=10\), and \(I(10)=\log 11\).

## Final answer

\[
\log{\left(11 \right)}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `(x**10 - 1)/log(x)`, `answer_sympy` is `log(11)`, and `limits` is `['0', '1']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
