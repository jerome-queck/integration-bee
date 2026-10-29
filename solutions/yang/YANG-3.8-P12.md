# YANG-3.8-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 12, printed p. 68 (PDF p. 69).

## Problem

∫_0^{∞} dx/sqrt(1+sqrt(e^x))

\[
\frac{1}{\sqrt{e^{\frac{x}{2}} + 1}}
\]

## Solution

Put \(u=e^{x/2}\), then \(w=\sqrt{1+u}\). The integral becomes \(4\int_{\sqrt{2}}^\infty dw/(w^2-1)\). The antiderivative \(\log|(w-1)/(w+1)|\) gives \(-2\log(\sqrt{2}-1)+2\log(\sqrt{2}+1)\).

## Final answer

\[
- 2 \log{\left(-1 + \sqrt{2} \right)} + 2 \log{\left(1 + \sqrt{2} \right)}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `1/sqrt(exp(x/2) + 1)`, `answer_sympy` is `-2*log(-1 + sqrt(2)) + 2*log(1 + sqrt(2))`, and `limits` is `['0', 'oo']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
