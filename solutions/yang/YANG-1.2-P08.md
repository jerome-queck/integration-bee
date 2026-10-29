# YANG-1.2-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 8, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac1x\left(\ln x+\frac{1}{\ln x}\right)\,dx.\]

## Solution

Let \(u=\ln x\). Then \(du=dx/x\), so the integral is \(\frac12(\ln x)^2+\ln|\ln x|\).

## Final answer

\[\frac12(\ln x)^2+\ln|\ln x|.\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(log(x) + 1/log(x))/x` and `answer_sympy` `log(x)**2/2 + log(Abs(log(x)))`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
