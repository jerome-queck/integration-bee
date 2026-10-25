# R1-2025-Online-Q18

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 18)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 18)
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi/2}\frac{x}{\tan x}\,dx.
\]

## Solution

The integrand is \(x\cot x\). Integration by parts gives
\[
\bigl[x\ln(\sin x)\bigr]_0^{\pi/2}-\int_0^{\pi/2}\ln(\sin x)\,dx.
\]
The boundary term vanishes. The log-sine integral equals \(-(\pi/2)\ln 2\), so the original integral equals \((\pi/2)\ln 2\). The mark scheme prints \((\pi/2)\ln 2\).

## Final answer

\[
\frac\pi2\ln 2.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q18`. SymPy differentiates \(x\ln(\sin x)\) to \(\ln(\sin x)+x\cot x\). A quadrature of \(\ln(\sin x)\) on \((0,\pi/2)\) matches \(-(\pi/2)\ln 2\).
