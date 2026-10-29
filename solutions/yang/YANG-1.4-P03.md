# YANG-1.4-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.4 Basic Exponential Functions, practice list item 3, printed p. 11 (PDF p. 12).
- The practice list prints no final. Worked source: derived in this note.

## Problem

The printed integral is

\[\int_{0}^{\infty}\frac{2^{x}+3^{x}}{5^{x}}\,dx.\]

## Solution

For a positive base, \(a^{x}=\exp(x\log a)\). The printed quotient equals \(e^{-x\log(5/2)}+e^{-x\log(5/3)}\). For \(c=\log(5/2)>0\), the primitive of \(e^{-cx}\) is \(-e^{-cx}/c\). That primitive is \(0\) at infinity and \(-1/c\) at \(0\), so the ray equals \(1/c\). The same holds for \(\log(5/3)\).

## Final answer

\[\dfrac{1}{\log(5/2)}+\dfrac{1}{\log(5/3)}.\]

## SymPy self-check

`verify/yang_certificates.py` evaluates the printed quotient by splitting `(2**x + 3**x)/5**x` into `exp(-x*log(5/2)) + exp(-x*log(5/3))` and integrating each ray. `verify/pack_gate.py` re-proves the stored pair. The catalog stores `sympy_expr` `(2**x + 3**x)/5**x` and `answer_sympy` `1/(-log(2) + log(5)) + 1/(-log(3) + log(5))`. `make check` re-proves that stored pair.
