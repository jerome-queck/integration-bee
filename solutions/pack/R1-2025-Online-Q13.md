# R1-2025-Online-Q13

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 13)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 13)
- The catalog row is not changed.

## Problem

\[
\int_{|x|+|y|+|z|\le 1}\bigl\lceil x^{2}+y^{2}+z^{2}\bigr\rceil\,dx\,dy\,dz.
\]

## Solution

Inside the region, except at the origin,
\[
0<x^{2}+y^{2}+z^{2}\le(|x|+|y|+|z|)^{2}\le 1,
\]
so the ceiling is \(1\). The region is the regular octahedron with vertices at unit distance on the axes. Its volume is eight times the tetrahedron \(\{x,y,z\ge 0,\,x+y+z\le 1\}\), whose volume is \(1/6\), hence \(4/3\). The solutions PDF reaches the same value from the edge-length formula \((\sqrt{2}/3)(\sqrt{2})^{3}\). The mark scheme prints \(4/3\).

## Final answer

\[
\dfrac{4}{3}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q13`. SymPy checks \((a+b+c)^{2}-a^{2}-b^{2}-c^{2}=2(ab+bc+ca)\) for nonnegative \(a,b,c\) and evaluates eight times the tetrahedron volume as \(4/3\).
