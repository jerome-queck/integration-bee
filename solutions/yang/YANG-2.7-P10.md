# YANG-2.7-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 10, printed p. 46 (PDF p. 47).

## Problem

∫_0^1 asin(sqrt(x))/sqrt(1-x) dx

\[
\frac{\operatorname{asin}{\left(\sqrt{x} \right)}}{\sqrt{1 - x}}
\]

## Solution

Put \(\sqrt{x}=\sin\theta\), so \(\theta\) runs from \(0\) to \(\pi/2\). The integral becomes \(\int_0^{\pi/2}2\theta\sin\theta\,d\theta=2\).

## Final answer

\[
2
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `asin(sqrt(x))/sqrt(1 - x)`, `answer_sympy` is `2`, and `limits` is `['0', '1']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
