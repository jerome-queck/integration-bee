# R1-2022-Oxford-Q15

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 15)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}x^{2n}e^{-x^{2}}\,dx,\qquad n\in\mathbb{Z}_{\ge 0}.
\]

## Solution

Set \(t=x^{2}\). Then \(dx=dt/(2\sqrt{t})\) and the integral is
\[
\frac12\int_0^{\infty}t^{n-1/2}e^{-t}\,dt=\frac12\Gamma\Bigl(n+\frac12\Bigr).
\]
The half-integer evaluation \(\Gamma(n+1/2)=(2n)!\sqrt{\pi}/(4^{n}n!)\) is the form printed by the mark scheme,
\[
\frac{(2n)!}{4^{n}n!}\cdot\frac{\sqrt{\pi}}{2}.
\]

## Final answer

\[
\dfrac{(2n)!\,\sqrt{\pi}}{4^{n}\,n!\,2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q15`. SymPy simplifies \(\Gamma(n+1/2)/2-(2n)!\sqrt{\pi}/(4^{n}n!\,2)\) to \(0\).
