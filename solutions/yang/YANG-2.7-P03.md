# YANG-2.7-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 3, printed p. 46 (PDF p. 47).

## Problem

∫_{-1}^{1} asin(sqrt(1-x^2)) dx

\[
\operatorname{asin}{\left(\sqrt{1 - x^{2}} \right)}
\]

## Solution

Put \(x=\cos\theta\), so \(\theta\) runs from \(0\) to \(\pi\) as \(x\) runs from \(1\) down to \(-1\), and \(\sqrt{1-x^2}=\sin\theta\). The integral is \(\int_0^\pi\operatorname{asin}(\sin\theta)\sin\theta\,d\theta\). On \([0,\pi/2]\) the arcsine is \(\theta\), and on \([\pi/2,\pi]\) it is \(\pi-\theta\). Each piece equals \(\int_0^{\pi/2}\theta\sin\theta\,d\theta=1\), so the value is \(2\).

## Final answer

\[
2
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `asin(sqrt(1 - x**2))`, `answer_sympy` is `2`, and `limits` is `['-1', '1']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
