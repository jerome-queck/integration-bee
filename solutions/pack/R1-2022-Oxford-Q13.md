# R1-2022-Oxford-Q13

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 13)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_1^{\sqrt{3}}\frac{\arctan x+\operatorname{arccot}x}{x}\,dx.
\]

## Solution

For \(x>0\), \(\arctan x+\operatorname{arccot}x=\pi/2\). The integral is
\[
\frac{\pi}{2}\int_1^{\sqrt{3}}\frac{dx}{x}=\frac{\pi}{2}\ln\sqrt{3}=\frac{\pi}{4}\ln 3.
\]
The mark scheme prints \((\pi/4)\ln 3\).

## Final answer

\[
\dfrac{\pi}{4}\ln 3.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q13`. SymPy checks that the derivative of \(\arctan x+\operatorname{arccot}x\) is \(0\) and that the value at \(1\) is \(\pi/2\), then evaluates \((\pi/2)\int_1^{\sqrt{3}}dx/x=(\pi/4)\ln 3\).
