# R1-2022-Oxford-Q26

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 26)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{-\infty}^{\infty}\frac{\cos x}{\cosh x}\,dx.
\]

## Solution

The integrand is the real part of \(e^{ix}\operatorname{sech}x\). The poles of \(\operatorname{sech}z\) in the upper half-plane are \(z_{n}=i(\pi/2+n\pi)\) for \(n\ge 0\), with residue \(1/\sinh z_{n}=-i(-1)^{n}\). Closing the contour and summing the geometric series of residues produces
\[
\int_{-\infty}^{\infty}\frac{e^{ix}}{\cosh x}\,dx=\pi\operatorname{sech}\frac{\pi}{2}.
\]
The imaginary part is odd, so the cosine integral has the same value. The mark scheme prints \(\pi\operatorname{sech}(\pi/2)\).

## Final answer

\[
\pi\operatorname{sech}\dfrac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q26`. A quadrature of \(\cos x/\cosh x\) over \(\mathbb{R}\) matches \(\pi\operatorname{sech}(\pi/2)\) to within \(10^{-10}\).
