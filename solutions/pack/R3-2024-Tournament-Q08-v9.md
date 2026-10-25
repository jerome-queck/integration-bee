# R3-2024-Tournament-Q08-v9

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 3, problem 8, slide 190)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 192)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.3, problem 2)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{\lfloor x\rfloor!\,(2\lfloor x\rfloor)!!}{(2\lceil x\rceil-1)!}\,dx.
\]

## Solution

On \([n,n+1)\) one has \(\lfloor x\rfloor=n\) and \(\lceil x\rceil=n+1\), so the denominator is \((2n+1)!\). The double factorial \((2n)!!=2^{n}n!\), and the general term is

\[
\frac{n!\,2^{n}n!}{(2n+1)!}=2^{n}B(n+1,n+1)=2^{n}\int_{0}^{1}x^{n}(1-x)^{n}\,dx.
\]

Summing the geometric series inside the integral gives

\[
\int_{0}^{1}\frac{1}{1-2x(1-x)}\,dx=\int_{0}^{1}\frac{2}{1+(2x-1)^{2}}\,dx=\bigl[\arctan(2x-1)\bigr]_{0}^{1}=\frac{\pi}{2}.
\]

The answer slide prints \(\pi/2\).

## Final answer

\[
\dfrac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q08_v9`. SymPy checks that the factorial term equals \(2^{n}B(n+1,n+1)\) and evaluates \(\int_{0}^{1}2/(1+(2x-1)^{2})\,dx=\pi/2\).
