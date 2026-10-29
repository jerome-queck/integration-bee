# YANG-1.5-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 15, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (\sec(\tan x)\sec x)^{2}\,dx.\]

## Solution

The integrand is \(\sec^{2}(\tan x)\sec^{2}x\). Set \(u=\tan x\). Then \(du=\sec^{2}x\,dx\), and \(\int\sec^{2}u\,du=\tan(\tan x)\).

## Final answer

\[\tan(\tan x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `sec(x)**2*sec(tan(x))**2` and `answer_sympy` `tan(tan(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
