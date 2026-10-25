# R1-2025-Online-Q14

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 14)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 14)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{2\pi}\sin(\sin x+2025 x)\,dx.
\]

## Solution

King's substitution \(x\mapsto 2\pi-x\) in the solutions PDF uses \(2025\cdot 2\pi\in 2\pi\mathbb{Z}\) and \(\sin(2\pi-x)=\sin(-x)\):
\[
\sin(\sin(2\pi-x)+2025(2\pi-x))=-\sin(\sin x+2025 x).
\]
The integral equals its own negative, so it is \(0\). The same PDF also shifts by \(\pi\) and uses that \(2025\) is odd, which makes the shifted integrand odd on \([-\pi,\pi]\). The mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q14`. SymPy simplifies the sum of the integrand and its reflection \(x\mapsto 2\pi-x\) to \(0\).
