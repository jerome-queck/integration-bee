# YANG-1.12-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 01, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-2}^{2} |x^{2}-1|\,dx.
\]

## Solution

Split at the roots of \(x^{2}-1\). On \([-2,-1]\) and \([1,2]\) the integrand is \(x^{2}-1\); on \([-1,1]\) it is \(1-x^{2}\). Each piece is a polynomial, and the four evaluations add to 4.

## Final answer

\[
4.
\]

## SymPy self-check

`verify/pack_gate.py` proves `Abs(x**2 - 1)` against `4` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
