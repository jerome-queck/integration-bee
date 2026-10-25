# R1-2022-Oxford-Q08

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 8)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi/2}x\prod_{i=1}^{\infty}\cos\Bigl(\frac{x}{2^{i}}\Bigr)\,dx.
\]

## Solution

The double-angle formula iterates to
\[
\sin x=2^{n}\sin\Bigl(\frac{x}{2^{n}}\Bigr)\prod_{i=1}^{n}\cos\Bigl(\frac{x}{2^{i}}\Bigr).
\]
As \(n\to\infty\), \(\sin(x/2^{n})/(x/2^{n})\to 1\), so the infinite product is \(\sin x/x\) on \((0,\pi/2)\). The integrand is \(\sin x\), and
\[
\int_0^{\pi/2}\sin x\,dx=1.
\]
The mark scheme prints \(1\).

## Final answer

\[
1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q08`. SymPy checks the finite product identity through \(n=6\) and evaluates \(\int_0^{\pi/2}\sin x\,dx=1\).
