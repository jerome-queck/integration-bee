# R3-2024-Tournament-Q05-v3

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 2, problem 5, answer slide 29)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 29)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.2, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 29, not the integral. Slide 29 is the answer reveal for Battle 1, Fight 2, problem 5:

\[
\int_{1}^{\infty}\frac{1}{x\bigl(x^{\ln 2048}+1\bigr)}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q05`.

## Solution

Factor \(x^{\ln 2048}\) from the second factor of the denominator:

\[
\frac{1}{x(x^{\ln 2048}+1)}=\frac{1}{x^{\ln 2048+1}\bigl(1+x^{-\ln 2048}\bigr)}.
\]

Set \(u=1+x^{-\ln 2048}\). Then \(u(1)=2\), \(u(\infty)=1\), and \(u'=-\ln(2048)\,x^{-\ln 2048-1}\). The integral becomes

\[
\frac{1}{\ln 2048}\int_{1}^{2}\frac{1}{u}\,du=\frac{\ln 2}{\ln 2048}.
\]

Since \(2048=2^{11}\), this equals \(1/11\). The answer slide prints \(1/11\).

## Final answer

\[
\dfrac{1}{11}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q05_v3`. That check runs `check_r3_2024_tournament_q05` for `R3-2024-Tournament-Q05`. SymPy checks the substitution factor \(1/u\), the endpoints \(u(1)=2\) and \(u(\infty)=1\), and \(\ln 2/\ln 2048=1/11\).
