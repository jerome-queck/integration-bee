# R3-2024-Tournament-Q05-v11

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 2, problem 5, answer slide 176)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 176)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.2, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 176, not the integral. Slide 176 is the answer reveal for Battle 4, Fight 2, problem 5:

\[
\int\frac{e^{W(x)}}{x^{2}}\,dx,
\]

where \(W\) is the principal branch of the Lambert \(W\) function, so \(W(x)e^{W(x)}=x\). Answers in terms of \(W(x)\) are acceptable.

The integral itself is catalogued as `R3-2024-Tournament-Q05-v9`.

## Solution

Set \(w=W(x)\), so \(x=we^{w}\) and \(dx=e^{w}(w+1)\,dw\). Substitution gives

\[
\frac{e^{w}}{(we^{w})^{2}}\cdot e^{w}(w+1)\,dw=\frac{w+1}{w^{2}}\,dw.
\]

Integrating produces

\[
\ln|w|-\frac{1}{w}+C=\ln|W(x)|-\frac{1}{W(x)}+C.
\]

The answer slide prints the same antiderivative.

## Final answer

\[
\ln|W(x)|-\dfrac{1}{W(x)}+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q05_v11`. That check runs `check_r3_2024_tournament_q05_v9` for `R3-2024-Tournament-Q05-v9`. SymPy substitutes \(x=we^{w}\) and integrates \((w+1)/w^{2}\).
