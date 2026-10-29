# YANG-3.8-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 10, printed p. 68 (PDF p. 69).

## Problem

∫ x(x+1)/((x-1)x+1) dx

\[
\frac{x \left(x + 1\right)}{x \left(x - 1\right) + 1}
\]

## Solution

The denominator is \(x^2-x+1\). Polynomial division gives
\[
\frac{x^2+x}{x^2-x+1}=1+\frac{2x-1}{x^2-x+1}.
\]
The second numerator is the derivative of the denominator, so an antiderivative is \(x+\log(x^2-x+1)\).

## Final answer

\[
x + \log{\left(x^{2} - x + 1 \right)}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `x*(x + 1)/(x*(x - 1) + 1)`, `answer_sympy` is `x + log(x**2 - x + 1)`, and `limits` is `[]`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
