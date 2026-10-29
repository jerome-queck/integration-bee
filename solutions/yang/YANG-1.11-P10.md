# YANG-1.11-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 10, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ (1/x^5) √((x^4+1)/x^4) dx

## Solution

Set t = 1/x^4. Then x^(−5) dx = −dt/4 and the square root is √(1+t), so the integral is −(1/6)(1+1/x^4)^(3/2).

## Final answer

\[
- \frac{\sqrt{x^{4} + 1}}{6 x^{2}} - \frac{\sqrt{x^{4} + 1}}{6 x^{6}}
\]

Stored `answer_sympy`: `-sqrt(x**4 + 1)/(6*x**2) - sqrt(x**4 + 1)/(6*x**6)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
