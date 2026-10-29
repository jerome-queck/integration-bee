# YANG-1.2-P02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 2, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \tan(x)\sec^2(x)\,dx.\]

## Solution

Let \(u=\tan x\). Then \(du=\sec^2(x)\,dx\), so the integral is \(\frac12\tan^2(x)\).

## Final answer

\[\frac12\tan^2(x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `tan(x)*sec(x)**2` and `answer_sympy` `tan(x)**2/2`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
