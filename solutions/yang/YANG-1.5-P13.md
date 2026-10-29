# YANG-1.5-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 13, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (\tan x+\sec x)^{2}\,dx.\]

## Solution

Expand as \(2\sec^{2}x+2\sec x\tan x-1\). The integral is \(2\tan x+2\sec x-x\).

## Final answer

\[2\tan x+2\sec x-x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(tan(x) + sec(x))**2` and `answer_sympy` `-x + 2*tan(x) + 2*sec(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
