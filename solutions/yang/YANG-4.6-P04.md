# YANG-4.6-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §4.6 Reverse Quotient Rule, Logarithm Example, printed p. 81 (PDF p. 82).

## Problem

∫ ln(x)/(1+ln(x))^2 dx

\[
\frac{\log{\left(x \right)}}{\left(\log{\left(x \right)} + 1\right)^{2}}
\]

## Solution

Differentiate \(x/(1+\log x)\). The quotient rule produces
\[
\frac{(1+\log x)-1}{(1+\log x)^2}=\frac{\log x}{(1+\log x)^2}.
\]
That is the integrand. The previous example on the page, \(\int x e^{2x}/(2x+1)^2\,dx\), and the following trigonometric example are separate displayed integrals.

## Final answer

\[
\frac{x}{\log{\left(x \right)} + 1}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `log(x)/(log(x) + 1)**2`, `answer_sympy` is `x/(log(x) + 1)`, and `limits` is `[]`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
