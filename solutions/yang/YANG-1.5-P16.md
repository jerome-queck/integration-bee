# YANG-1.5-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 16, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{1}{\sec x+\tan x}\,dx.\]

## Solution

Multiply by \(\sec x-\tan x\). The denominator becomes \(1\), and the integrand is \(\sec x-\tan x\). Its integral is \(\log(1+\sin x)\).

## Final answer

\[\log(1+\sin x).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `1/(tan(x) + sec(x))` and `answer_sympy` `log(sin(x) + 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
