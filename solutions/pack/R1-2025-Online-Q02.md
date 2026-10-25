# R1-2025-Online-Q02

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 2)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 2)
- The catalog row is not changed.

## Problem

\[
\int_0^\infty\sin(\pi\lfloor x\rfloor)\,dx.
\]

## Solution

On each interval \([k,k+1)\) the floor equals the integer \(k\), and \(\sin(\pi k)=0\). Splitting the improper integral therefore gives
\[
\sum_{k=0}^\infty\int_k^{k+1}\sin(\pi k)\,dx=0.
\]
The mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q02`. SymPy checks \(\sin(\pi k)=0\) for an integer symbol \(k\) and evaluates the zero integral on a unit interval.
