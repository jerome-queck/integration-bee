# YANG-1.20-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 07, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{0}^{1} \frac{\ln(1+x+x^{2})}{x}\,dx.
\]

## Solution

On \((0,1)\), \(1+x+x^{2}=(1-x^{3})/(1-x)\), so the integrand is \((\ln(1-x^{3})-\ln(1-x))/x\). \(\operatorname{Li}_{1}(x)=-\ln(1-x)\), and \(\operatorname{Li}_{2}(x)-\operatorname{Li}_{2}(x^{3})/3\) differentiates to that quotient. From \(0\) to \(1\) it equals \(\pi^{2}/9\).

## Final answer

\[
\frac{\pi^{2}}{9}.
\]

## SymPy self-check

`verify/yang_worked_check.py` differentiates \(\operatorname{Li}_{2}(x)-\operatorname{Li}_{2}(x^{3})/3\) and evaluates it from \(0\) to \(1\). `verify/pack_gate.py` proves `log(x**2 + x + 1)/x` against `pi**2/9`.
