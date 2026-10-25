# R1-2022-Oxford-Q17

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 17)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1\sqrt{-\ln x}\,dx.
\]

## Solution

Set \(x=e^{-u}\). The integral becomes
\[
\int_0^{\infty}u^{1/2}e^{-u}\,du=\Gamma\Bigl(\frac32\Bigr)=\frac{\sqrt{\pi}}{2}.
\]
The mark scheme prints \(\sqrt{\pi}/2\).

## Final answer

\[
\dfrac{\sqrt{\pi}}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q17`. SymPy evaluates \(\int_0^{\infty}\sqrt{u}\,e^{-u}\,du=\sqrt{\pi}/2\).
