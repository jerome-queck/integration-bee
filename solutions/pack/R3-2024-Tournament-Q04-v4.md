# R3-2024-Tournament-Q04-v4

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 2, problem 4, slide 71)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 73)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.2, problem 1)
- The catalog row is not changed.

## Problem

\[
\int\frac{x^{2}-1}{x^{3}+x}\ln\left(x^{3}+\frac{1}{x^{3}}+3\left(x+\frac{1}{x}\right)\right)dx.
\]

## Solution

The argument of the logarithm is a cube:

\[
x^{3}+\frac{1}{x^{3}}+3\left(x+\frac{1}{x}\right)=\left(x+\frac{1}{x}\right)^{3}.
\]

The integral is therefore

\[
3\int\frac{x^{2}-1}{x^{3}+x}\ln\left(x+\frac{1}{x}\right)dx.
\]

Set \(u=\ln(x+1/x)\). Then

\[
du=\frac{x^{2}-1}{x^{3}+x}\,dx,
\]

and the integral is \(\int 3u\,du\):

\[
\frac32\left(\ln\left(x+\frac{1}{x}\right)\right)^{2}+C.
\]

The answer slide prints the same antiderivative.

## Final answer

\[
\dfrac{3}{2}\left(\ln\left(x+\dfrac{1}{x}\right)\right)^{2}+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q04_v4`. SymPy checks the cube identity, the derivative of \(u\), and the derivative of \(\frac32 u^{2}\).
