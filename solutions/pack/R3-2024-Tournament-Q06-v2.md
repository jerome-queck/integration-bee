# R3-2024-Tournament-Q06-v2

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 2, problem 6, answer slide 34)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 34)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.2, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 34 prints the final value of Battle 1, Fight 2, problem 6:

\[
\int_{0}^{2\pi}\frac{1}{\bigl(1+2^{\sin x}\bigr)\bigl(1+2^{\cos x}\bigr)}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q06`.

## Solution

The reflection \(x\mapsto 2\pi-x\) replaces \(2^{\sin x}\) by \(2^{-\sin x}\) and leaves \(2^{\cos x}\) unchanged. Because

\[
\frac{1}{1+2^{-\sin x}}=\frac{2^{\sin x}}{1+2^{\sin x}},
\]

the reflected integrand is the original integrand with the first factor replaced by that quotient. Averaging the two copies cancels the sine factor:

\[
I=\frac12\int_{0}^{2\pi}\frac{1}{1+2^{\cos x}}\,dx.
\]

Shift the second half of that integral by \(\pi\). Then \(2^{\cos(x+\pi)}=2^{-\cos x}\), and

\[
\frac{1}{1+2^{\cos x}}+\frac{1}{1+2^{-\cos x}}=1.
\]

Hence \(I=\pi/2\). The answer slide prints \(\pi/2\).

## Final answer

\[
\dfrac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q06_v2`. That check runs `check_r3_2024_tournament_q06` for `R3-2024-Tournament-Q06`. SymPy checks \(1/(1+2^{-s})=2^{s}/(1+2^{s})\) and that the cosine pair sums to \(1\).
