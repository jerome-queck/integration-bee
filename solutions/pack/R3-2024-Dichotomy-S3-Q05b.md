# R3-2024-Dichotomy-S3-Q05b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 5b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 5b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 5b)
- The catalog row is not changed.

## Problem

\[\int_{-\infty}^{\infty}\sin\bigl(x^{2}+x\sqrt{3\pi}+\pi\bigr)\,dx.\]

## Solution

Completing the square, the solutions PDF writes the phase as \((x+\sqrt{3\pi}/2)^{2}+\pi/4\). The integral equals \[\sqrt{2}\int_{0}^{\infty}\bigl(\sin(x^{2})+\cos(x^{2})\bigr)\,dx.\]

The two Fresnel integrals agree, and the value is \(\sqrt{\pi}\).

## Final answer

\[\sqrt{\pi}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q05b`. SymPy checks the completed square and evaluates \(\sqrt{2}\cdot 2\int_{0}^{\infty}\sin(x^{2})\,dx=\sqrt{\pi}\).
