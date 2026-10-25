# R3-2024-Tournament-Q06-v5

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 2, problem 6, answer slide 83)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 83)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.2, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 83 prints the final value of Battle 2, Fight 2, problem 6:

\[
\int_{-2024}^{2025}f_{\infty}(x)\,dx,
\]

where \(f_{0}(x)=2x/(1+x^{2})\), \(f_{n}=f_{n-1}\circ f_{n-1}\) for each integer \(n\ge 1\), and \(f_{\infty}=\lim_{k\to\infty}f_{k}\).

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q06-v4`.

## Solution

A fixed point of \(t\mapsto 2t/(1+t^{2})\) satisfies \(t=2t/(1+t^{2})\), so \(t(t-1)(t+1)=0\). The only possible values of the pointwise limit are therefore \(-1\), \(0\), and \(1\).

The sign of \(f_{0}\) selects the limit: \(f_{0}(x)\) has the sign of \(x\), and iterating the double-angle map \(2t/(1+t^{2})\) keeps that sign. Thus \(f_{\infty}(x)=\operatorname{sgn}(x)\), with value \(0\) at \(x=0\). The integral is the length of the positive part minus the length of the negative part:

\[
2025-2024=1.
\]

The answer slide prints \(1\).

## Final answer

\[
1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q06_v5`. That check runs `check_r3_2024_tournament_q06_v4` for `R3-2024-Tournament-Q06-v4`. SymPy factors \(f(1+f^{2})-2f=f(f-1)(f+1)\) and checks \(2025-2024=1\).
