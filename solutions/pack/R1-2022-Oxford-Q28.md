# R1-2022-Oxford-Q28

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 28)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1\frac{x-1}{(x+1)\ln x}\,dx.
\]

## Solution

For \(x>0\) with \(x\neq 1\),
\[
\frac{x-1}{\ln x}=\int_0^1 x^{s}\,ds,
\]
and the two sides agree at \(x=1\) by continuity. Therefore
\[
I=\int_0^1\int_0^1\frac{x^{s}}{1+x}\,dx\,ds.
\]
Expand \(1/(1+x)=\sum_{n\ge 0}(-1)^{n}x^{n}\) and integrate in \(x\):
\[
I=\sum_{n\ge 0}(-1)^{n}\ln\Bigl(\frac{n+2}{n+1}\Bigr)=\ln\prod_{m\ge 0}\frac{(2m+2)^{2}}{(2m+1)(2m+3)}.
\]
The product is the Wallis product for \(\pi/2\). The mark scheme prints \(\ln(\pi/2)\). This is not the 2025 integrand \(x(x-1)/((x+1)\ln x)\).

## Final answer

\[
\ln\dfrac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q28`. SymPy checks \(\int_0^1 x^{s}\,ds=(x-1)/\ln x\) away from \(x=1\), and a quadrature of the original integrand matches \(\ln(\pi/2)\).
