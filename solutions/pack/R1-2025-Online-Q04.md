# R1-2025-Online-Q04

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 4)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 4)
- The catalog row is not changed.

## Problem

\[
\int_0^a e^{i\pi/2}\,dz.
\]

## Solution

Euler's identity gives \(e^{i\pi/2}=i\), so the integrand is the constant \(i\):
\[
\int_0^a i\,dz=ai.
\]
The mark scheme prints \(ai\).

## Final answer

\[
ai.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q04`. SymPy checks \(e^{i\pi/2}=i\) and evaluates \(\int_0^a i\,dz\).
