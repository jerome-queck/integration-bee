# YANG-4.4-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §4.4 Advanced King's Rule, A Crazy Example, printed p. 76 (PDF p. 77).

## Problem

∫_{1/4}^{3/4} f(f(x)) dx, where f(t)=4^t/(2+4^t)

\[
\frac{4^{\frac{4^{x}}{4^{x} + 2}}}{4^{\frac{4^{x}}{4^{x} + 2}} + 2}
\]

## Solution

Let \(f(t)=4^t/(2+4^t)\). For a generic real \(z\), clearing the sum gives \(f(z)+f(1-z)-1=0\), and the same identity at \(z=f(x)\) gives \(f(f(x))+f(1-f(x))-1=0\). Also \(1-f(x)=f(1-x)\), so \(f(f(x))+f(f(1-x))=1\). On \([1/4,3/4]\) the map \(x\mapsto 1-x\) swaps the endpoints and has derivative \(-1\), so the two copies of the integral are equal. Their sum is the length \(1/2\), and each copy is \(1/4\).

## Final answer

\[
\frac{1}{4}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `4**(4**x/(4**x + 2))/(4**(4**x/(4**x + 2)) + 2)`, `answer_sympy` is `1/4`, and `limits` is `['1/4', '3/4']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
