# YANG-1.5-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 6, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \tan^{2}x\,dx.\]

## Solution

Use \(\tan^{2}x=\sec^{2}x-1\). The integral is \(\tan x-x\).

## Final answer

\[\tan x-x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `tan(x)**2` and `answer_sympy` `-x + tan(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
