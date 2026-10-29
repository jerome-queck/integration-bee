# YANG-2.6-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 12, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/yang_certificates.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \frac{1}{\sqrt{3 \sin{\left(x \right)} + \cos{\left(x \right)}}}\,dx.
\]

## Solution

\(3\sin x+\cos x=\sqrt{10}\sin(x+\arctan(1/3))\). With \(t=\tan(\theta/2)\) and \(s=\sqrt{t}\), \(1/\sqrt{\sin\theta}\) pulls back to \(2\sqrt{2}/\sqrt{1+s^{4}}\). The \(s\)-derivative of \(\sqrt{2}\,F(2\arctan s\mid 1/2)\) is that pullback. The factor \(10^{-1/4}\) restores the phase shift, and the catalog stores the expanded coefficient \(2^{1/4}5^{3/4}/5\).

## Final answer

\[
\frac{\sqrt[4]{2} \cdot 5^{\frac{3}{4}} F\left(2 \operatorname{atan}{\left(\sqrt{\tan{\left(\frac{x}{2} + \frac{\operatorname{atan}{\left(\frac{1}{3} \right)}}{2} \right)}} \right)}\middle| \frac{1}{2}\right)}{5}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `1/sqrt(3*sin(x) + cos(x))`. `answer_sympy` is `2**(1/4)*5**(3/4)*elliptic_f(2*atan(sqrt(tan(x/2 + atan(1/3)/2))), 1/2)/5`. `verify/yang_certificates.py` checks the phase identity, the Weierstrass Jacobian, and the elliptic derivative. `make check` re-proves the stored row.
