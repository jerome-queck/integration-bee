# YANG-3.8-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 8, printed p. 68 (PDF p. 69).
- Both square roots are the principal branch.

## Problem

∫ from -1 to 1 of \(\sqrt{x+\sqrt{x^2-1}}+\sqrt{x-\sqrt{x^2-1}}\,dx\)

\[
\sqrt{x - \sqrt{x^{2} - 1}} + \sqrt{x + \sqrt{x^{2} - 1}}
\]

## Solution

Set \(x=\cos\theta\) with \(\theta\) running from \(\pi\) down to 0. On \((0,\pi)\), \(\sin\theta>0\), so \(\sqrt{x^2-1}=i\sin\theta\). The two insides are \(e^{i\theta}\) and \(e^{-i\theta}\).

The real and imaginary parts of the principal square roots are \(\cos(\operatorname{atan2}(\sin\theta,\cos\theta)/2)\) and \(\sin(\operatorname{atan2}(\sin\theta,\cos\theta)/2)\), and the same formulas with \(-\sin\theta\). On \((0,\pi)\) those arguments equal \(\theta\) and \(-\theta\), because each derivative is constant and the value at \(\pi/2\) matches. The sum is \(2\cos(\theta/2)\).

The integral becomes \(\int_0^{\pi}2\cos(\theta/2)\sin\theta\,d\theta\). The double-angle formula and \(u=\cos(\theta/2)\) turn it into \(8\int_0^1 u^2\,du=8/3\).

## Final answer

\[
\frac{8}{3}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `sqrt(x - sqrt(x**2 - 1)) + sqrt(x + sqrt(x**2 - 1))`, `answer_sympy` is `8/3`, and `limits` is `['-1', '1']`. `verify/yang_l8.py` checks the principal-branch reduction.
