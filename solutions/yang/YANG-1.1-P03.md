# YANG-1.1-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.1 Basic Integration, textbook list item 3, printed p. 7 (PDF p. 8).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{1+\sqrt{x}}{x}\,dx.\]

## Solution

Split the quotient as \(x^{-1}+x^{-1/2}\). The antiderivative is \(\ln|x|+2\sqrt{x}\).

## Final answer

\[\ln|x|+2\sqrt{x}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(sqrt(x) + 1)/x` and `answer_sympy` `2*sqrt(x) + log(Abs(x))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
