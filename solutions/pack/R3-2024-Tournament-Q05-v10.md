# R3-2024-Tournament-Q05-v10

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 2, problem 5, answer slide 176)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 176)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.2, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 176 prints the final value of Battle 4, Fight 2, problem 5:

\[
\int\frac{e^{W(x)}}{x^{2}}\,dx,
\]

where \(W\) is the principal Lambert function. The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q05-v9`. Answers in terms of \(W(x)\) are acceptable.

## Solution

Set \(w=W(x)\), so \(x=we^{w}\) and \(dx=e^{w}(w+1)\,dw\). The integrand becomes \((w+1)/w^{2}\), and

\[
\int\frac{w+1}{w^{2}}\,dw=\ln|W(x)|-\frac{1}{W(x)}+C.
\]

Slide 176 prints that antiderivative.

## Final answer

\[
\ln|W(x)|-\dfrac{1}{W(x)}+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q05_v10`. That check runs the Lambert substitution for `R3-2024-Tournament-Q05-v9`.
