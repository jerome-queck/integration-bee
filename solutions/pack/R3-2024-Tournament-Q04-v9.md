# R3-2024-Tournament-Q04-v9

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 2, problem 4, answer slide 122)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 122)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.2, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 122, not the integral. Slide 122 is the answer reveal for Battle 3, Fight 2, problem 4:

\[
\int_{-\infty}^{\infty}\frac{2^{\lfloor 2^{x}\rfloor+x}}{3^{2^{\lfloor 2^{x}\rfloor}}+1}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q04-v7`.

## Solution

Set \(y=2^{x}\). Then \(dy=y\ln 2\,dx\) and the factor \(2^{x}=y\) cancels, leaving

\[
\frac{1}{\ln 2}\int_{0}^{\infty}\frac{2^{\lfloor y\rfloor}}{3^{2^{\lfloor y\rfloor}}+1}\,dy=\frac{1}{\ln 2}\sum_{n=0}^{\infty}\frac{2^{n}}{3^{2^{n}}+1}.
\]

The general term telescopes:

\[
\frac{2^{n}}{3^{2^{n}}+1}=\frac{2^{n}}{3^{2^{n}}-1}-\frac{2^{n+1}}{3^{2^{n+1}}-1}.
\]

The sum is the first term, \(1/(3-1)=1/2\). Therefore the integral equals

\[
\frac{1}{2\ln 2}.
\]

The answer slide prints \(1/(2\ln 2)\).

## Final answer

\[
\dfrac{1}{2\ln 2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q04_v9`. That check runs `check_r3_2024_tournament_q04_v7` for `R3-2024-Tournament-Q04-v7`. SymPy checks the telescoping identity at \(n=0,1,2,3,4,5\) and simplifies \(\frac12/\ln 2\).
