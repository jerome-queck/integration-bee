# YANG-2.5-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.5 Integration by Parts, practice list item 12, printed p. 44 (PDF p. 45).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=45).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/pack_gate.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int x^{2} \operatorname{asec}{\left(x \right)}\,dx.
\]

## Solution

Integrate by parts with u = arcsec(x). For x > 1 the remaining integral is (1/3) ∫ sec(θ)^3 dθ after x = sec(θ). The gate checks the derivative with x positive.

## Final answer

\[
\frac{x^{3} \operatorname{asec} x}{3} - \frac{|x|\sqrt{x^{2}-1}}{6} - \frac{\log\bigl(|x|+\sqrt{x^{2}-1}\bigr)}{6}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `x**2*asec(x)`. `answer_sympy` is `x**3*asec(x)/3 - Abs(x)*sqrt(x**2 - 1)/6 - log(Abs(x) + sqrt(x**2 - 1))/6`. `verify/pack_gate.py` differentiates that antiderivative and recovers the integrand. `make check` re-proves the stored row.
