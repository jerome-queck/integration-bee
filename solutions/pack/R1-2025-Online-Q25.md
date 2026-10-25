# R1-2025-Online-Q25

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 25)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 25)
- The catalog row is not changed.

## Problem

\[
\int_0^{25}\sqrt{1+x\sqrt{1+(x+1)\sqrt{1+(x+2)\sqrt{\cdots}}}}\,dx.
\]

## Solution

The solutions PDF truncates the nest with the identity \((x+n+1)^{2}=1+(x+n)(x+n+2)\) and collapses it. Each step removes one radical, and the infinite nest equals \(x+1\) for \(x>0\). Therefore
\[
\int_0^{25}(x+1)\,dx=\frac{675}{2}.
\]
The mark scheme prints \(675/2\).

## Final answer

\[
\dfrac{675}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q25`. SymPy checks \((x+n+1)^{2}=1+(x+n)(x+n+2)\) and evaluates \(\int_0^{25}(t+1)\,dt=675/2\).
