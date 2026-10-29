# YANG-3.8-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 7, printed p. 68 (PDF p. 69).

## Problem

∫_{-π/2}^{π/2} (sin(x)+cos(x)+tan(x))/sec(x)^2 dx

\[
\frac{\sin{\left(x \right)} + \cos{\left(x \right)} + \tan{\left(x \right)}}{\sec^{2}{\left(x \right)}}
\]

## Solution

Multiply through by \(\cos^2 x\). The terms \(\sin x\cos^2 x\) and \(\sin x\cos x\) are odd, so they vanish on \([-\pi/2,\pi/2]\). The even term is \(2\int_0^{\pi/2}\cos^3 x\,dx=2\int_0^1(1-u^2)\,du=4/3\).

## Final answer

\[
\frac{4}{3}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `(sin(x) + cos(x) + tan(x))/sec(x)**2`, `answer_sympy` is `4/3`, and `limits` is `['-pi/2', 'pi/2']`. `verify/pack_gate.py` proves it by an antiderivative derivative or by exact definite evaluation.
