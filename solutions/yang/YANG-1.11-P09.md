# YANG-1.11-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 9, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫_0^1 x^2(2x−1)^7 dx

## Solution

Set u = 2x−1. The interval [0, 1] becomes [−1, 1], and only the even part of (u+1)^2 u^7 survives. Its integral is 1/18.

## Final answer

\[
\frac{1}{18}
\]

Stored `answer_sympy`: `1/18`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `definite` comparison of the stored fields. The stored value is the exact evaluation of the printed limits. `make check` re-proves those fields. Numeric agreement is not the proof.
