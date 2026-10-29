# YANG-2.3-P16

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.3 Basic Forced U-Substitutions, practice item 16, printed p. 42 (PDF p. 43).
- The practice list prints no final. This note derives the final of the printed integrand.

## Problem

Printed integral: ∫_{ln 2}^{∞} ln(1-e^{-x})/(e^x-1) dx.

Catalog integrand `log(1 - exp(-x))/(exp(x) - 1)`, limits `['log(2)', 'oo']`, display `\frac{\log{\left(1 - e^{- x} \right)}}{e^{x} - 1}`.

## Solution

Let \(u=e^{-x}\). Then \(dx=-du/u\), the limit \(x=\ln 2\) becomes \(u=1/2\), and \(x\to\infty\) becomes \(u\to 0\). Also \(e^x-1=(1-u)/u\), so
\[
\int_{1/2}^{0}\frac{\ln(1-u)}{(1-u)/u}\Bigl(-\frac{du}{u}\Bigr)
=\int_0^{1/2}\frac{\ln(1-u)}{1-u}\,du.
\]
The further substitution \(t=1-u\) produces
\[
\int_{1/2}^{1}\frac{\ln t}{t}\,dt=\frac12(\ln t)^2\Big|_{1/2}^{1}=-\frac12(\ln 2)^2.
\]

## Final answer

The catalog stores `answer_sympy` as `-log(2)**2/2` and `answer_latex` as `- \frac{\log{\left(2 \right)}^{2}}{2}`.

## SymPy self-check

`verify/pack_gate.py` proves this definite row by an exact closed evaluation. `make check` re-proves the stored fields and does not open the PDF.
