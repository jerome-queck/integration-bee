# YANG-1.15-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 17, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{\pi/6} \sqrt{\frac{1}{1-\sin x}+\frac{1}{1+\sin x}}\,dx.
\]

## Solution

The expression under the square root simplifies to \(2/\cos^{2} x\). On \([0,\pi/6]\), \(\cos\) has minimum \(\sqrt{3}/2>0\), so the integrand is \(\sqrt{2}\sec x\). The antiderivative \(\sqrt{2}\ln(\sec x+\tan x)\) evaluates to \(\sqrt{2}\ln 3/2\).

## Final answer

\[
\frac{\sqrt{2} \log{\left(3 \right)}}{2}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(1/(sin(x) + 1) + 1/(1 - sin(x)))` against `sqrt(2)*log(3)/2` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
