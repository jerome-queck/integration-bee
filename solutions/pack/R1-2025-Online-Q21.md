# R1-2025-Online-Q21

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 21)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 21)
- The catalog row is not changed.

## Problem

\[
\int_0^1\cdots\int_0^1\max(x_1,\ldots,x_{2025})\,dx_1\cdots dx_{2025}.
\]

## Solution

For each index \(i\), let \(V_i\) be the part of the unit cube on which \(x_i\) is the maximum. Those regions meet on lower-dimensional ties. On \(V_i\) the integrand is \(x_i\), and the slice at height \(x_i\) is a cube of side \(x_i\) in the other \(2024\) coordinates. The integral is
\[
\sum_{i=1}^{2025}\int_0^1 x_i\cdot x_i^{2024}\,dx_i=2025\int_0^1 x^{2025}\,dx=\frac{2025}{2026}.
\]
The mark scheme prints \(2025/2026\).

## Final answer

\[
\frac{2025}{2026}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q21`. SymPy evaluates \(2025\int_0^1 x^{2025}\,dx=2025/2026\).
