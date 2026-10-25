# R1-2022-Oxford-Q19

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 19)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1\frac{\ln(1+x)}{x}\,dx.
\]

## Solution

On \([0,1)\),
\[
\frac{\ln(1+x)}{x}=\sum_{n\ge 1}(-1)^{n-1}\frac{x^{n-1}}{n}.
\]
Integrating term by term produces \(\sum_{n\ge 1}(-1)^{n-1}/n^{2}=\pi^{2}/12\). The endpoint \(x=1\) does not change the value. The mark scheme prints \(\pi^{2}/12\).

## Final answer

\[
\dfrac{\pi^{2}}{12}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q19`. SymPy sums \(\sum_{n\ge 1}(-1)^{n-1}/n^{2}\) to \(\pi^{2}/12\).
