# YANG-2.3-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 11, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_0^{ln 10} e^x √(e^x-1)/(e^x+8) dx.

Catalog integrand `sqrt(exp(x) - 1)*exp(x)/(exp(x) + 8)`, limits `['0', 'log(10)']`, display `\frac{\sqrt{e^{x} - 1} e^{x}}{e^{x} + 8}`.

## Solution

Let \(t=\sqrt{e^x-1}\), so \(e^x=t^2+1\) and \(e^x\,dx=2t\,dt\). The limits \(x=0\) and \(x=\ln 10\) become \(t=0\) and \(t=3\). The integrand simplifies to
\[
\int_0^3\frac{2t^2}{t^2+9}\,dt=2\int_0^3\Bigl(1-\frac{9}{t^2+9}\Bigr)\,dt
=2\bigl[t-3\arctan(t/3)\bigr]_0^3=6-\frac{3\pi}{2}.
\]

## Final answer

The catalog stores `answer_sympy` as `6 - 3*pi/2` and `answer_latex` as `6 - \frac{3 \pi}{2}`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
