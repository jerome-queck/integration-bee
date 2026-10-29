# YANG-1.5-P19

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 19, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{(\sec x-\csc x)(\sec x+\csc x)}{\tan x+\cot x}\,dx.\]

## Solution

The numerator is \(\sec^{2}x-\csc^{2}x=-4\cos(2x)/\sin^{2}(2x)\), and \(\tan x+\cot x=2/\sin(2x)\). The quotient is \(-2\cot(2x)\). The integral is \(-\log(\sin(2x))\).

## Final answer

\[-\log(\sin(2x)).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(-csc(x) + sec(x))*(csc(x) + sec(x))/(tan(x) + cot(x))` and `answer_sympy` `-log(sin(2*x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
