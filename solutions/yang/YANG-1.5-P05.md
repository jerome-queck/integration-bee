# YANG-1.5-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.5 Basic Trig Integrals, practice list item 5, printed p. 12 (PDF p. 13).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \tan x\sec^{3}x\,dx.\]

## Solution

Set \(u=\sec x\). Then \(du=\sec x\tan x\,dx\), and the integrand is \(u^{2}\,du\). The integral is \(\sec^{3}x/3\).

## Final answer

\[\dfrac{\sec^{3}x}{3}.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `tan(x)*sec(x)**3` and `answer_sympy` `sec(x)**3/3`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
