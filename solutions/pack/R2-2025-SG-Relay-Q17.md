# R2-2025-SG-Relay-Q17

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf`, PDF p. 5 (relay 17).
- Printed answer: none in the pack. The value below is derived in this note.
- Worked source: derived in this note.
- Catalog contract: `product_indefinite`, on the real positive domain \(x>0\), with \(C>0\).

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
C\,x^{x^{2}/2}e^{-x^{2}/4}\qquad(C>0,\ x>0).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q17`. SymPy checks that the logarithmic derivative of the derived multiplicative primitive is \(x\ln x\).

## Catalog gate

`verify/pack_handoff_f_integrals.py` checks a positive product primitive by
\[
\frac{F'(x)}{F(x)}=\ln(x^x)=x\ln x\qquad(x>0).
\]
On the connected interval \((0,\infty)\), any two positive solutions have constant positive ratio, so this is exactly the multiplicative-constant freedom. The explicit `product_indefinite` kind preserves the meaning of the differential in the exponent. The ordinary `indefinite` kind continues to use an additive constant and an ordinary derivative.

The product contract accepts positive multiples of the displayed primitive and equivalent exponential forms. It requires a continuous first derivative throughout \((0,\infty)\), so a multiplier with jumps between different constants cannot pass through a merely formal derivative identity. It rejects additive shifts, zero and negative multiples, an explicitly nonpositive \(C\), and ordinary antiderivatives whose logarithmic derivative is not \(x\log x\).
