# YANG-1.5-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 4, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (\tan x\sec x)^{2}\,dx.\]

## Solution

The integrand is \(\tan^{2}x\sec^{2}x\). Set \(u=\tan x\). Then \(du=\sec^{2}x\,dx\), so the integral is \(\tan^{3}x/3\).

## Final answer

\[\dfrac{\tan^{3}x}{3}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `tan(x)**2*sec(x)**2` and `answer_sympy` `tan(x)**3/3`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
