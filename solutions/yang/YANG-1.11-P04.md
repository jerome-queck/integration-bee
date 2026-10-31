# YANG-1.11-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 4, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.
- Transcription: corrected from the page image after audit A1 (31 Oct 2026).

## Problem

∫ x/√(x−1) dx

\[
\frac{x}{\sqrt{x - 1}}
\]

## Solution

Set u = x − 1. Then x/√(x−1) = (u+1)/√u = √u + 1/√u. Integrate termwise: (2/3)u^{3/2} + 2√u = (2/3)(x+2)√(x−1).

## Final answer

\[
\frac{\sqrt{x - 1} \left(2 x + 4\right)}{3}
\]

Stored `answer_sympy`: `2*(x + 2)*sqrt(x - 1)/3`.

## SymPy self-check

`verify/pack_gate.py` proves this row by differentiating the stored antiderivative back to the stored integrand on x > 1. The value was also re-checked with mpmath at 40 digits.
