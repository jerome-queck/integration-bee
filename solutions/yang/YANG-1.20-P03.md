# YANG-1.20-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 03, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{2\pi} \frac{1}{\sin^{4} x+\cos^{4} x}\,dx.
\]

## Solution

\(\sin^{4} x+\cos^{4} x=(3+\cos 4x)/4\), so the integrand is \(4/(3+\cos 4x)\). The substitution \(u=4x\) produces four periods of \(1/(3+\cos u)\). Each period integrates to \(\pi\sqrt{2}/2\), and four of them give \(2\pi\sqrt{2}\).

## Final answer

\[
2 \sqrt{2} \pi.
\]

## SymPy self-check

`verify/pack_gate.py` proves `1/(sin(x)**4 + cos(x)**4)` against `2*sqrt(2)*pi` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
