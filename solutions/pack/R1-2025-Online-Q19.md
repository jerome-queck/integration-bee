# R1-2025-Online-Q19

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 19)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 19)
- The catalog row is not changed.

## Problem

\[
\int_0^{2025}\Biggl(\frac{x}{\sqrt{x+\sqrt{x+\sqrt{x+\cdots}}}}-\sqrt{x-\sqrt{x-\sqrt{x-\cdots}}}\Biggr)\,dx.
\]

## Solution

Let \(z=\sqrt{x+\sqrt{x+\cdots}}\) and \(y=\sqrt{x-\sqrt{x-\cdots}}\), taking the positive roots. Then \(z^{2}=x+z\) and \(y^{2}=x-y\), so
\[
z=\frac{1+\sqrt{1+4x}}{2},\qquad y=\frac{-1+\sqrt{1+4x}}{2}.
\]
These satisfy \(x/z=y\). The integrand is identically \(0\), and the integral is \(0\). The solutions PDF reduces the same two radicals to a difference that cancels. The mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q19`. SymPy checks \(z^{2}=x+z\), \(y^{2}=x-y\), and \(x/z=y\).
