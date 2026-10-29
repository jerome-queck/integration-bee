# YANG-2.7-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §2.7 Intermediate Trig-Substitution, practice item 5, printed p. 46 (PDF p. 47).

## Problem

∫_0^{∞} sqrt(1+sqrt(1+x^2))/(1+x^2) dx

\[
\frac{\sqrt{\sqrt{x^{2} + 1} + 1}}{x^{2} + 1}
\]

## Solution

Put \(x=\tan\theta\), with \(\theta\) from \(0\) to \(\pi/2\). Since \(\cos\theta>0\) on \((0,\pi/2)\), \(\sqrt{1+\tan^2\theta}=\sec\theta\), and the integral becomes \(\int_0^{\pi/2}\sqrt{1+\sec\theta}\,d\theta\). The half-angle identities \(1+\cos\theta=2\cos^2(\theta/2)\) and \(\cos\theta=1-2\sin^2(\theta/2)\), with \(\cos(\theta/2)>0\), give
\[
\sqrt{1+\sec\theta}\,d\theta=\frac{2\sqrt{2}\,du}{\sqrt{1-2u^2}},\qquad u=\sin(\theta/2).
\]
Then \(u=\sin\phi/\sqrt{2}\) runs from \(0\) to \(\pi/2\) in \(\phi\), and the integrand collapses to \(2\). The value is \(\pi\). `verify/yang_l8.py` checks each of those identities before returning \(\pi\).

## Final answer

\[
\pi
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `sqrt(sqrt(x**2 + 1) + 1)/(x**2 + 1)`, `answer_sympy` is `pi`, and `limits` is `['0', 'oo']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
