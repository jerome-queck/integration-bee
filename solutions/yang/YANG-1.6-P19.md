# YANG-1.6-P19

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.6 Basic Integration by Parts, practice item 19, printed p. 13 (PDF p. 14).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=14).
- The guide lists the integral and does not print a final.
- Worked source: derived in this note.

## Problem

\[
\int \sqrt{e^{x}(x^{2}+6x+9)}\,dx.
\]

## Solution

The radicand is \(e^{x}(x+3)^{2}\). Because \(e^{x/2}>0\), the integrand is \(e^{x/2}|x+3|\). On \(x\ge -3\) the antiderivative \((2x+2)e^{x/2}\) has derivative \(e^{x/2}(x+3)\). On \(x<-3\) the antiderivative \((-2x-2)e^{x/2}\) has derivative \(-e^{x/2}(x+3)\). Those pieces differ by \(8e^{-3/2}\) at \(x=-3\). Subtracting that constant on the left piece makes the two values equal, so the primitive is continuous.

## Final answer

\[
\begin{cases}
(2x+2)e^{x/2} & x\ge -3,\\
(-2x-2)e^{x/2}-8e^{-3/2} & x<-3.
\end{cases}
\]

## SymPy self-check

`verify/piecewise_primitive.py` differentiates each piece by the ordinary derivative test and checks that both pieces equal \(-4e^{-3/2}\) at \(x=-3\). The quotient \(2(x^{2}+4x+3)e^{x/2}/\sqrt{x^{2}+6x+9}\) jumps there, so it is not the stored primitive.
