# R3-2024-Dichotomy-S3-Q06a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 6a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 6a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 6a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\pi/4}\bigl(\cos^{8}x-\sin^{8}x\bigr)\,dx.\]

## Solution

Factor \(\cos^{8}x-\sin^{8}x=(\cos^{4}x+\sin^{4}x)\cos(2x)\). The solutions PDF reduces this to \(\cos(2x)\bigl(1-\sin^{2}(2x)/2\bigr)\). Then \[\left[\frac{\sin(2x)}{2}-\frac{\sin^{3}(2x)}{12}\right]_{0}^{\pi/4}=\frac{5}{12}.\]

## Final answer

\[\dfrac{5}{12}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q06a`. SymPy checks the factorisation and evaluates the antiderivative from \(0\) to \(\pi/4\).
