# YANG-1.5-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 11, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\tan x+\cot x}{\sin x\cos x}\,dx.\]

## Solution

\(\tan x+\cot x=1/(\sin x\cos x)\), so the integrand is \(1/(\sin^{2}x\cos^{2}x)=\sec^{2}x+\csc^{2}x\). The integral is \(\tan x-\cot x\).

## Final answer

\[\tan x-\cot x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(tan(x) + cot(x))/(sin(x)*cos(x))` and `answer_sympy` `tan(x) - cot(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
