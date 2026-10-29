# YANG-2.7-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 7, printed p. 46 (PDF p. 47).

## Problem

∫_{√2}^{∞} dx/(x^2 (x^2-1)^{3/2})

\[
\frac{1}{x^{2} \left(x^{2} - 1\right)^{\frac{3}{2}}}
\]

## Solution

Put \(x=\sec\theta\), so \(\theta\) runs from \(\pi/4\) to \(\pi/2\). The integral becomes \(\int\cos^3\theta/\sin^2\theta\,d\theta=\int(\cos\theta/\sin^2\theta-\cos\theta)\,d\theta=-\csc\theta-\sin\theta\). The endpoint difference is \(-2+3\sqrt{2}/2\).

## Final answer

\[
-2 + \frac{3 \sqrt{2}}{2}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `1/(x**2*(x**2 - 1)**(3/2))`, `answer_sympy` is `-2 + 3*sqrt(2)/2`, and `limits` is `['sqrt(2)', 'oo']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
