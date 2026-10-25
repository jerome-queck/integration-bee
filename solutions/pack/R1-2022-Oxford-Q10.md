# R1-2022-Oxford-Q10

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 10)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi/2}\frac{1}{\tan^{\sqrt{2}}x+1}\,dx.
\]

## Solution

For any real exponent \(a\),
\[
\frac{1}{\tan^{a}x+1}+\frac{1}{\tan^{a}(\pi/2-x)+1}=1,
\]
because \(\tan(\pi/2-x)=\cot x\). The printed exponent is \(\sqrt{2}\), and the pairing does not use that value. Therefore
\[
2I=\int_0^{\pi/2}1\,dx=\frac{\pi}{2},
\]
so \(I=\pi/4\). The mark scheme prints \(\pi/4\).

## Final answer

\[
\dfrac{\pi}{4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q10`. SymPy checks \(1/(t+1)+1/(1/t+1)=1\) for \(t>0\), that \(\cot x=1/\tan x\), and evaluates \(\int_0^{\pi/2}(1/2)\,dx=\pi/4\).
