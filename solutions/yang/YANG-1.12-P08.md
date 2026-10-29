# YANG-1.12-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 08, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{1}^{e} \frac{x+1}{|x-\ln x|+\ln x}\,dx.
\]

## Solution

The derivative of \(x-\ln x\) is \((x-1)/x\), which is nonnegative on \([1,e]\). The function therefore increases from \(1\) to \(e-1\), so the absolute value is the expression itself and the integrand simplifies to \((x+1)/x\). Its antiderivative \(x+\ln x\) runs from \(1\) to \(e+1\), a difference of \(e\).

## Final answer

\[
e.
\]

## SymPy self-check

`verify/pack_gate.py` proves `(x + 1)/(log(x) + Abs(x - log(x)))` against `E` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
