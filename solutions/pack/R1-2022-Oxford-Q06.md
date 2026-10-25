# R1-2022-Oxford-Q06

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 6)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}\frac{1}{1+e^{ax}}\,dx,\qquad a>0.
\]

## Solution

Set \(u=e^{-ax}\), so \(dx=-du/(au)\). The limits run from \(1\) to \(0\), and
\[
\frac{1}{1+e^{ax}}\,dx=\frac{du}{a(1+u)}
\]
after reversing them. The integral is \((\ln 2)/a\). The mark scheme prints \((\ln 2)/a\).

## Final answer

\[
\dfrac{\ln 2}{a}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q06`. SymPy evaluates \(\int_0^{\infty}dx/(1+e^{ax})\) as \((\ln 2)/a\).
