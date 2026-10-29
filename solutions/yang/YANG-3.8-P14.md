# YANG-3.8-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 14, printed p. 68 (PDF p. 69).

## Problem

∫ tan(2x)/tan(x)^2 dx

\[
\frac{\tan{\left(2 x \right)}}{\tan^{2}{\left(x \right)}}
\]

## Solution

Use \(\tan(2x)=2\tan x/(1-\tan^2 x)\) and \(u=\tan x\), so \(dx=du/(1+u^2)\). The integrand becomes the rational function \(2/(u(1-u^2)(1+u^2))\). Partial fractions integrate to the stored combination of logarithms in \(\tan x\), and differentiating that combination returns the integrand.

## Final answer

\[
- \frac{\log{\left(\tan{\left(x \right)} - 1 \right)}}{2} - \frac{\log{\left(\tan{\left(x \right)} + 1 \right)}}{2} - \frac{\log{\left(\tan^{2}{\left(x \right)} + 1 \right)}}{2} + 2 \log{\left(\tan{\left(x \right)} \right)}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `tan(2*x)/tan(x)**2`, `answer_sympy` is `-log(tan(x) - 1)/2 - log(tan(x) + 1)/2 - log(tan(x)**2 + 1)/2 + 2*log(tan(x))`, and `limits` is `[]`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
