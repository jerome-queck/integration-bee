# R1-2022-Oxford-Q04

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 4)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int e^{x+e^{x}}\,dx.
\]

## Solution

The chain rule gives
\[
\frac{d}{dx}e^{e^{x}}=e^{x}e^{e^{x}}=e^{x+e^{x}}.
\]
The mark scheme prints \(e^{e^{x}}\).

## Final answer

\[
e^{e^{x}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q04`. SymPy differentiates \(e^{e^{x}}\) and obtains \(e^{x+e^{x}}\).
