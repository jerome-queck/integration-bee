# YANG-1.20-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.20 Special Wildcard, practice item 1, printed p. 37 (PDF p. 38).
- Printed answer: absent.
- Worked source: derived in this note.
- Transcription: `pdftoppm` of PDF p. 38 shows the radical bar covering \(x+1\). The bar runs from the left of \(x\) through the right of \(1\) and stops where the closing parenthesis begins. The text layer had split the radicand as \(\sqrt{x}+1\).

## Problem

\[
\int_{0}^{\infty}\frac{\ln\sqrt{x+1}}{x\sqrt{x}}\,dx.
\]

## Solution

For \(x>0\),
\[
\ln\sqrt{x+1}=\frac12\ln(1+x),\qquad x\sqrt{x}=x^{3/2}.
\]
The integrand is therefore
\[
\frac12\frac{\ln(1+x)}{x^{3/2}}.
\]
SymPy simplifies the difference of those two expressions to 0. The comparison integral
\[
\int_{0}^{\infty}\frac{\ln(1+x)}{x^{3/2}}\,dx
\]
evaluates to \(2\pi\), so this integral is \(\pi\).

The text-layer radicand \(\ln(\sqrt{x}+1)\) is a different integrand. The gate does not accept \(\pi\) for it.

## Final answer

\[
\pi.
\]

Stored `answer_sympy`: `pi`.

## SymPy self-check

`verify/pack_gate.py` proves `log(sqrt(x + 1))/x**(3/2)` against `pi` (definite). The check is an exact closed evaluation of the stored integrand. The factor-of-two identity above is an algebraic simplification, and \(\int_0^\infty \ln(1+x)/x^{3/2}\,dx=2\pi\) is the same integrator's exact value. Numeric agreement is not the proof.
