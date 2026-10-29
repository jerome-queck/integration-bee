# YANG-1.2-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 17, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \tan x\,dx.\]

## Solution

Write \(\tan x=\sin x/\cos x\). Let \(u=\cos x\). Then \(du=-\sin x\,dx\), so the integral is \(-\ln|\cos x|\).

## Final answer

\[-\ln|\cos x|.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `tan(x)` and `answer_sympy` `-log(Abs(cos(x)))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
