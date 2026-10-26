# R3-2024-Dichotomy-S3-Q06b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 6b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 6b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 6b)
- The catalog row is `verify: sympy`.

## Problem

\[\int_{0}^{\pi/4}\bigl(\cos^{6}x-\sin^{6}x\bigr)\,dx.\]

## Solution

Factor \(\cos^{6}x-\sin^{6}x=\cos(2x)\bigl(1-\sin^{2}(2x)/4\bigr)\). Then \[\left[\frac{\sin(2x)}{2}-\frac{\sin^{3}(2x)}{24}\right]_{0}^{\pi/4}=\frac{11}{24}.\]

## Final answer

\[\dfrac{11}{24}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q06b`. SymPy checks the reduced integrand and evaluates the antiderivative from \(0\) to \(\pi/4\).
