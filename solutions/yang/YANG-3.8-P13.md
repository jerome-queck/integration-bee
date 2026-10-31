# YANG-3.8-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 13, printed p. 68 (PDF p. 69).
- Printed answer: absent.
- Worked source: derived in this note.
- Transcription: corrected from the page image after audit A1 (31 Oct 2026).

## Problem

∫_0^{9} e^{√(1+√x)} dx

\[
e^{\sqrt{\sqrt{x} + 1}}
\]

## Solution

Substitute x = u², then u = w² − 1. The integral becomes ∫_1^2 4(w³ − w)e^w dw. An antiderivative of (w³ − w)e^w is (w³ − 3w² + 5w − 5)e^w, which is e² at w = 2 and −2e at w = 1. The value is 4e² + 8e.

## Final answer

\[
8 e + 4 e^{2}
\]

Stored `answer_sympy`: `4*exp(2) + 8*E`.

## SymPy self-check

`verify/yang_worked_check.py` checks both substitutions, the antiderivative and the endpoint values exactly. The value was also re-checked with mpmath at 40 digits.
