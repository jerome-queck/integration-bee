# R1-2022-Oxford-Q30

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 30)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^1\frac{\sin(\log x)-\log x}{\log^{2}x}\,dx.
\]

## Solution

On this sheet \(\log\) is the natural logarithm. Set \(x=e^{-u}\). The integral becomes
\[
J(1)=\int_0^{\infty}e^{-u}\frac{u-\sin u}{u^{2}}\,du.
\]
Differentiating twice in a parameter \(s>0\) gives
\[
J''(s)=\int_0^{\infty}e^{-su}(u-\sin u)\,du=\frac{1}{s^{2}}-\frac{1}{s^{2}+1}.
\]
The right derivative that vanishes at infinity is \(J'(s)=\pi/2-1/s-\arctan s\). Then \(J(\infty)=0\), so
\[
J(1)=\int_1^{\infty}\Bigl(\frac{1}{w}+\arctan w-\frac{\pi}{2}\Bigr)\,dw=\frac{\ln 2}{2}+\frac{\pi}{4}-1.
\]
The antiderivative is \(w\arctan w-\ln(1+w^{2})/2-(\pi/2)w+\ln w\). The mark scheme prints \((\ln 2)/2+\pi/4-1\).

## Final answer

\[
\dfrac{\ln 2}{2}+\dfrac{\pi}{4}-1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q30`. SymPy differentiates \(-1/w-\arctan w\) back to \(1/w^{2}-1/(w^{2}+1)\) and evaluates the improper integral of the first derivative as \((\ln 2)/2+\pi/4-1\).
