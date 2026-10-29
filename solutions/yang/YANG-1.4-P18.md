# YANG-1.4-P18

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 18, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int_{0}^{\infty}\frac{1+\sqrt{1-e^{-x}}}{e^{x}}\,dx.\]

## Solution

Set \(t=e^{-x}\). Then \(dx=-dt/t\), and \(x\) from \(0\) to \(\infty\) sends \(t\) from \(1\) to \(0\). The integrand \((1+\sqrt{1-e^{-x}})e^{-x}\,dx\) becomes \(-(1+\sqrt{1-t})\,dt\). Reversing the limits gives \(\int_{0}^{1}(1+\sqrt{1-t})\,dt=1+\bigl[-\frac23(1-t)^{3/2}\bigr]_{0}^{1}=1+\frac23=\frac53\).

## Final answer

\[\dfrac{5}{3}.\]

## SymPy self-check

`verify/pack_gate.py` proves this definite integral by closed evaluation. The catalog stores `sympy_expr` `(sqrt(1 - exp(-x)) + 1)*exp(-x)` and `answer_sympy` `5/3`. `make check` re-proves that stored pair.
