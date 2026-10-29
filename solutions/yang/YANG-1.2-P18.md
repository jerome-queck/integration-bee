# YANG-1.2-P18

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.2 Basic U-Substitution, list item 18, printed p. 8 (PDF p. 9).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int \frac{\sqrt{e^x}-\sqrt{e^{-x}}}{\sqrt{e^x}+\sqrt{e^{-x}}}\,dx.\]

## Solution

For real \(x\), \(\sqrt{e^x}=e^{x/2}\) and \(\sqrt{e^{-x}}=e^{-x/2}\). Multiplying numerator and denominator by \(e^{x/2}\) gives \((e^x-1)/(e^x+1)\). Let \(u=e^x\), so \(dx=du/u\). Then \(\int (u-1)/(u(u+1))\,du=\int(-1/u+2/(u+1))\,du=-x+2\ln(e^x+1)\).

## Final answer

\[-x+2\ln(e^x+1).\]

## SymPy self-check

`verify/pack_gate.py` proves this indefinite integral by differentiation. The catalog stores `sympy_expr` `(exp(x/2) - exp(-x/2))/(exp(x/2) + exp(-x/2))` and `answer_sympy` `-x + 2*log(exp(x) + 1)`. `make check` re-proves that stored pair. An additive constant differentiates to zero, so it is the same antiderivative.
