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
These algebraic values satisfy \(x/z=y\). The plus nest converges for \(x\ge 0\). The minus nest's iteration converges only for \(x>3/4\); on \([0,3/4]\) the iteration diverges, and the graded integrand is this closed form, which is identically \(0\). The integral of that closed form is \(0\). The mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q19`. SymPy checks \(z^{2}=x+z\), \(y^{2}=x-y\), and \(x/z=y\).
