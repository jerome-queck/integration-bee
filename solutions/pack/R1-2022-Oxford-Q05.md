# R1-2022-Oxford-Q05

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 5)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1\ln\Bigl(\frac{1+x}{1-x}\Bigr)\,dx.
\]

## Solution

The antiderivative is \((1+x)\ln(1+x)+(1-x)\ln(1-x)\), because the extra \(\pm 1\) terms cancel. Its limit from \(0\) to \(1\) is \(2\ln 2=\ln 4\). The mark scheme prints \(\ln 4\).

## Final answer

\[
\ln 4.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q05`. SymPy evaluates the definite integral as \(\ln 4\).
