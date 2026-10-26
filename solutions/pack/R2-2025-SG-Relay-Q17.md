# R2-2025-SG-Relay-Q17

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf`, PDF p. 5 (relay 17).
- Printed answer: none in the pack. The value below is derived in this note.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int (x^{x})^{dx},
\]

The PDF explicitly defines this as a product integral, with products in place of Riemann sums. Its notation places the differential in the exponent.

## Solution

The indefinite product integral is the exponential of the ordinary integral of the logarithm:
\[
\exp\Bigl(\int\ln(x^{x})\,dx\Bigr)=\exp\Bigl(\int x\ln x\,dx\Bigr).
\]
Integration by parts gives \(\int x\ln x\,dx=(x^{2}/2)\ln x-x^{2}/4\). Exponentiating produces
\[
C\,x^{x^{2}/2}e^{-x^{2}/4},
\]
with \(C>0\) because a product integral of a positive integrand is positive.

## Final answer

\[
C\,x^{x^{2}/2}e^{-x^{2}/4}\qquad(C>0).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q17`. SymPy checks that the logarithmic derivative of the derived multiplicative primitive is \(x\ln x\).

## Catalog gate

This row remains `verify: manual`. The current gate's indefinite contract checks the ordinary derivative, with an additive constant. A product primitive instead satisfies \(F'/F=\ln(x^x)\), with a positive multiplicative constant. Storing \(x^x\) as an ordinary integrand and accepting the product primitive would certify a different problem. A future product-integral contract can encode this closed form without weakening ordinary antiderivative verification.
