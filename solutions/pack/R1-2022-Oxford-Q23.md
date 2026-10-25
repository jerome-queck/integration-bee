# R1-2022-Oxford-Q23

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 23)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}\frac{e^{-x}\sin(ax)}{x}\,dx.
\]

## Solution

Both sides are odd in \(a\) and vanish at \(a=0\). For \(a>0\), differentiate in the parameter:
\[
\frac{d}{da}\int_0^{\infty}\frac{e^{-x}\sin(ax)}{x}\,dx=\int_0^{\infty}e^{-x}\cos(ax)\,dx=\frac{1}{1+a^{2}}.
\]
Integrating from \(0\) and using the value \(0\) at \(a=0\) gives \(\arctan a\). The mark scheme prints \(\arctan a\).

## Final answer

\[
\arctan a.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q23`. SymPy evaluates \(\int_0^{\infty}e^{-x}\cos(ax)\,dx=1/(1+a^{2})\) and checks that the derivative of \(\arctan a\) is the same kernel.
