# YANG-3.4-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.4 Advanced Trig-Substitution, triple-angle example, printed p. 61 (PDF p. 62).

## Problem

∫_0^{√3} atan((3x-x^3)/(1-3x^2)) dx

\[
\operatorname{atan}{\left(\frac{- x^{3} + 3 x}{1 - 3 x^{2}} \right)}
\]

## Solution

Put \(x=\tan\theta\), so \(\theta\) runs from \(0\) to \(\pi/3\). The triple-angle identity makes the integrand \(\operatorname{atan}(\tan 3\theta)\sec^2\theta\). The derivative of \(\operatorname{atan}(\tan y)\) is \(1\) wherever it is defined. On \([0,\pi/2)\) the value at \(0\) fixes \(\operatorname{atan}(\tan y)=y\), and on \((\pi/2,\pi]\) the value at \(3\pi/4\) fixes \(\operatorname{atan}(\tan y)=y-\pi\). Split at \(\theta=\pi/6\). The antiderivatives \(3\theta\tan\theta+3\log(\cos\theta)\) and \((3\theta-\pi)\tan\theta+3\log(\cos\theta)\) are legitimate because \(\cos\theta>0\) on \((0,\pi/3)\). Their endpoint sum is \(\pi/\sqrt{3}-\log 8\).

## Final answer

\[
- 3 \log{\left(2 \right)} + \frac{\sqrt{3} \pi}{3}
\]

## SymPy self-check

The catalog row is `verify: sympy`. `sympy_expr` is `atan((-x**3 + 3*x)/(1 - 3*x**2))`, `answer_sympy` is `-3*log(2) + sqrt(3)*pi/3`, and `limits` is `['0', 'sqrt(3)']`. `verify/yang_l8.py` returns this value after the identities above check exactly.
