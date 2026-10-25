# R3-2024-Dichotomy-S3-Q02b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 2b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 2b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 2b)
- The catalog row is not changed.

## Problem

\[\int_{1}^{\infty}e^{-\sqrt{\sqrt{x}-1}}\,dx.\]

## Solution

Set \(u=\sqrt{\sqrt{x}-1}\). Then \(x=(u^{2}+1)^{2}\) and \(dx=4u(1+u^{2})\,du\). The integral becomes \[4\int_{0}^{\infty}\bigl(u+u^{3}\bigr)e^{-u}\,du=4\bigl(\Gamma(2)+\Gamma(4)\bigr)=4(1+6)=28.\]

## Final answer

\[28.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q02b`. SymPy checks \(d(u^{2}+1)^{2}/du=4u(1+u^{2})\) and evaluates the two gamma integrals as \(28\).
