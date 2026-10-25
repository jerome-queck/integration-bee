# R1-2022-Oxford-Q16

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 16)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1(\sqrt{x}-x)^{3/2}\,dx.
\]

## Solution

Set \(t=\sqrt{x}\), so \(dx=2t\,dt\) and the integral is
\[
2\int_0^1 t^{5/2}(1-t)^{3/2}\,dt=2\,B\Bigl(\frac72,\frac52\Bigr)=2\frac{\Gamma(7/2)\Gamma(5/2)}{\Gamma(6)}=\frac{3\pi}{128}.
\]
The mark scheme prints \(3\pi/128\) and accepts an equal product of gamma values.

## Final answer

\[
\dfrac{3\pi}{128}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q16`. SymPy simplifies \(2\,\Gamma(7/2)\Gamma(5/2)/\Gamma(6)\) to \(3\pi/128\).
