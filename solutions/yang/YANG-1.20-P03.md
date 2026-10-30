# YANG-1.20-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 03, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{2\pi} \frac{1}{\sin^{4} x+\cos^{4} x}\,dx.
\]

## Solution

\(\sin^{4} x+\cos^{4} x=(3+\cos 4x)/4\), so the integrand is \(4/(3+\cos 4x)\). The substitution \(u=4x\) produces four periods of \(1/(3+\cos u)\). On each side of the jump of \(\tan(x/2)\), the antiderivative \(\arctan(\tan(x/2)/\sqrt{2})/\sqrt{2}\) evaluates to \(\pi\sqrt{2}/4\). One period is \(\pi\sqrt{2}/2\), and four periods give \(2\pi\sqrt{2}\).

## Final answer

\[
2 \sqrt{2} \pi.
\]

## SymPy self-check

`verify/yang_worked_check.py` differentiates \(\arctan(\tan(x/2)/\sqrt{2})/\sqrt{2}\) and evaluates the one-sided limits. `verify/pack_gate.py` proves `1/(sin(x)**4 + cos(x)**4)` against `2*sqrt(2)*pi`.
