# YANG-1.20-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 05, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{\infty} \frac{\arctan x}{x(\ln(x)^{2}+1)}\,dx.
\]

## Solution

The substitution \(x=e^{t}\) produces \(\int_{-\infty}^{\infty}\arctan(e^{t})/(t^{2}+1)\,dt\). The sum \(\arctan(e^{t})+\arctan(e^{-t})\) has derivative \(0\) and equals \(\pi/2\) at \(t=0\), so it is \(\pi/2\). Reflecting \(t\) therefore gives \(\tfrac12\cdot(\pi/2)\int_{-\infty}^{\infty} dt/(t^{2}+1)=\pi^{2}/4\).

## Final answer

\[
\frac{\pi^{2}}{4}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `atan(x)/(x*(log(x)**2 + 1))` against `pi**2/4` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
