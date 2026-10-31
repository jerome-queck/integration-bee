# YANG-2.6-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 1, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. Worked source: derived in this note.

## Problem

\[
\int \sqrt{\cos{\left(x \right)} + 1}\,dx.
\]

## Solution

Use \(1+\cos x=2\cos^2(x/2)\), so the integrand is \(\sqrt{2}\,|\cos(x/2)|\). On the piece where \(\lfloor x/(2\pi)+1/2\rfloor=k\), the derivative of \(2\sqrt{2}(-1)^k\sin(x/2)\) is the integrand. The expression \(2\sin x/\sqrt{1+\cos x}\) matches that piece between odd multiples of \(\pi\) and jumps by \(-4\sqrt{2}\) at each of them. The stored antiderivative adds \(4\sqrt{2}\lfloor x/(2\pi)+1/2\rfloor\), so the left and right limits agree.

## Final answer

\[
2(-1)^{\lfloor x/(2\pi)+1/2\rfloor}\sqrt{2}\sin(x/2)+4\sqrt{2}\lfloor x/(2\pi)+1/2\rfloor.
\]

The catalog omits a constant of integration.

## SymPy self-check

`verify/piecewise_primitive.py` checks the piece derivative and the joins. `verify/pack_gate.py` still differentiates the smooth piece \(2\sqrt{2}\sin(x/2)\) by the ordinary derivative test.
