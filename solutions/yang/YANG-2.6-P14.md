# YANG-2.6-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 14, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/yang_certificates.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int_{0}^{\pi/4} \log{\left(2 \cos^{2}{\left(x \right)} - 1 \right)} \cos{\left(x \right)}\,dx.
\]

## Solution

\(2\cos^{2}x-1=1-2\sin^{2}x\). Set \(u=\sin x\) and

\[
F(u)=u\log(1-2u^{2})-2u+\frac{1}{\sqrt{2}}\log\frac{1+\sqrt{2}\,u}{1-\sqrt{2}\,u}.
\]

SymPy simplifies \(F'(\sin x)\cos x\) to the integrand, \(F(0)=0\), and the limit of \(F(\sin x)\) as \(x\to(\pi/4)^{-}\) is \(\sqrt{2}(\log 2-1)\).

## Final answer

\[
\sqrt{2}\left(\log 2-1\right).
\]

## SymPy self-check

`sympy_expr` is `log(2*cos(x)**2 - 1)*cos(x)`. `answer_sympy` is `-sqrt(2) + sqrt(2)*log(2)`. The limits are `0` and `pi/4`. `verify/yang_certificates.py` checks the derivative identity and the endpoint limit. `make check` re-proves the stored row.
