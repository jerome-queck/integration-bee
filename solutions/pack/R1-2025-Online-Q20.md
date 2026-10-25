# R1-2025-Online-Q20

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 20)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 20)
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi/2}\int_0^1\exp\bigl(t+t^{\tan\theta}\bigr)\,dt\,d\theta.
\]

## Solution

Reflect \(\theta\mapsto\pi/2-\theta\), then substitute \(t=u^{\tan\theta}\) in that copy. Adding the result to the original integral produces
\[
I=\frac12\int_0^{\pi/2}\int_0^1\exp\bigl(t+t^{\tan\theta}\bigr)\bigl(1+\tan\theta\,t^{\tan\theta-1}\bigr)\,dt\,d\theta.
\]
The inner factor is the derivative of \(t+t^{\tan\theta}\). The substitution \(u=t+t^{\tan\theta}\) runs from \(0\) to \(2\), and
\[
I=\frac12\int_0^{\pi/2}\int_0^2 e^u\,du\,d\theta=\frac\pi4(e^2-1).
\]
The mark scheme prints \(\pi(e^2-1)/4\).

## Final answer

\[
\frac\pi4(e^2-1).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q20`. SymPy differentiates \(t+t^{\tan\theta}\) and evaluates \(\frac12\cdot(\pi/2)\int_0^2 e^u\,du\).
