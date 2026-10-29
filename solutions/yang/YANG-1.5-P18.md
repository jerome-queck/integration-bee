# YANG-1.5-P18

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 18, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int (1+\sin x)(1+\sec^{2}x)\,dx.\]

## Solution

Expand as \(1+\sec^{2}x+\sin x+\sin x\sec^{2}x\). Set \(u=\cos x\) in the last term: \(\int\sin x\sec^{2}x\,dx=\sec x\). The integral is \(x+\tan x-\cos x+\sec x\).

## Final answer

\[x+\tan x-\cos x+\sec x.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(sin(x) + 1)*(sec(x)**2 + 1)` and `answer_sympy` `x - cos(x) + tan(x) + sec(x)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
