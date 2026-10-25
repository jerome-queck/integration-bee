# R1-2022-Oxford-Q11

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 11)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1\sqrt{\frac{1+x}{1-x}}\,dx.
\]

## Solution

Set \(x=\cos 2\theta\), so \(\theta\) runs from \(\pi/4\) to \(0\) and \(\sqrt{(1+x)/(1-x)}=\cot\theta\). Then \(dx=-4\sin\theta\cos\theta\,d\theta\) and the integral becomes
\[
\int_0^{\pi/4}4\cos^{2}\theta\,d\theta=\int_0^{\pi/4}2(1+\cos 2\theta)\,d\theta=1+\frac{\pi}{2}.
\]
The mark scheme prints \(1+\pi/2\).

## Final answer

\[
1+\dfrac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q11`. SymPy evaluates the original definite integral as \(1+\pi/2\).
