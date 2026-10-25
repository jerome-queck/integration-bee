# R1-2022-Oxford-Q22

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 22)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int\frac{x^{2}+1}{x^{4}+1}\,dx.
\]

## Solution

On \((0,\infty)\),
\[
\frac{d}{dx}\left(\frac{1}{\sqrt{2}}\arctan\Bigl(\frac{x-1/x}{\sqrt{2}}\Bigr)\right)=\frac{x^{2}+1}{x^{4}+1}.
\]
The mark scheme prints that antiderivative.

## Final answer

\[
\dfrac{1}{\sqrt{2}}\arctan\Bigl(\dfrac{x-x^{-1}}{\sqrt{2}}\Bigr).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q22`. SymPy differentiates the printed antiderivative and simplifies the difference with \((x^{2}+1)/(x^{4}+1)\) to \(0\).
