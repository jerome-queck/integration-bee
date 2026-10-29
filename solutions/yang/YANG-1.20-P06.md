# YANG-1.20-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 06, printed p. 37 (PDF p. 38).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{3\sin x+4\cos x}{4\sin x+3\cos x}\,dx.
\]

## Solution

Write the numerator as \(\tfrac{7}{25}\) times the derivative of the denominator plus \(\tfrac{24}{25}\) times the denominator. The antiderivative is \(\tfrac{24}{25}x+\tfrac{7}{25}\ln(4\sin x+3\cos x)\).

## Final answer

\[
\frac{24 x}{25} + \frac{7 \log{\left(4 \sin{\left(x \right)} + 3 \cos{\left(x \right)} \right)}}{25}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `(3*sin(x) + 4*cos(x))/(4*sin(x) + 3*cos(x))` against `24*x/25 + 7*log(4*sin(x) + 3*cos(x))/25` (indefinite). The check differentiates the stored antiderivative.
