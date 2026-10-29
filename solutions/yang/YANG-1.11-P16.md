# YANG-1.11-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 16, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ sec(x) ln(sec(x)+tan(x)) dx

## Solution

Set u = sec x + tan x. Then du/u = sec x dx, so the integral is (1/2)(log u)^2.

## Final answer

\[
\frac{\log{\left(\tan{\left(x \right)} + \sec{\left(x \right)} \right)}^{2}}{2}
\]

Stored `answer_sympy`: `log(tan(x) + sec(x))**2/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
