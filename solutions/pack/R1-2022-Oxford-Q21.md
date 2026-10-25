# R1-2022-Oxford-Q21

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 21)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\infty}\frac{\ln(x^{2}+1)}{x^{2}+1}\,dx.
\]

## Solution

Set \(x=\tan\theta\). Then \(x^{2}+1=\sec^{2}\theta\) and the integral is
\[
\int_0^{\pi/2}\ln(\sec^{2}\theta)\,d\theta=-2\int_0^{\pi/2}\ln(\cos\theta)\,d\theta.
\]
The identity \(\ln(1+\tan^{2}\theta)+2\ln(\cos\theta)=0\) is the same substitution written without cancelling the square. The log-sine integral equals \(-(\pi/2)\ln 2\), so this integral equals \(\pi\ln 2\). The mark scheme prints \(\pi\ln 2\).

## Final answer

\[
\pi\ln 2.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q21`. SymPy reduces \(\ln(1+\tan^{2}\theta)+2\ln(\cos\theta)\) to \(0\), and a quadrature of \(\ln(\sin\theta)\) on \((0,\pi/2)\) matches \(-(\pi/2)\ln 2\).
