# R1-2025-Online-Q05

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 5)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 5)
- The catalog row is not changed.

## Problem

\[
\int_{-\pi/2}^{\pi/2}\frac{\cos x}{1+\sqrt[x]{e}}\,dx.
\]

## Solution

The \(x\)-th root of \(e\) is \(e^{1/x}\). Let \(f(x)=\cos x/(1+e^{1/x})\). The reflection \(x\mapsto -x\) in the solutions PDF gives a second copy with denominator \(1+e^{-1/x}\). Adding the copies,
\[
f(x)+f(-x)=\cos x,
\]
because the two rational factors of the exponential sum to \(1\). Therefore
\[
2I=\int_{-\pi/2}^{\pi/2}\cos x\,dx=2,
\]
and \(I=1\). The mark scheme prints \(1\).

## Final answer

\[
1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q05`. SymPy simplifies \(f(x)+f(-x)-\cos x\) to \(0\) for \(f(x)=\cos x/(1+e^{1/x})\) and evaluates \(\int_{-\pi/2}^{\pi/2}\cos x\,dx=2\).
