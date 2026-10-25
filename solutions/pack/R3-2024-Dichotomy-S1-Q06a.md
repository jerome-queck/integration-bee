# R3-2024-Dichotomy-S1-Q06a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 6a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 6a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 6a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\pi/2}\frac{\tan(\sin^{2}x)}{1-\tan(\sin^{2}x)\tan(\cos^{2}x)}\,dx.\]

## Solution

King's rule replaces \(\sin^{2}x\) by \(\cos^{2}x\) and leaves the denominator fixed. Averaging the two copies produces \[\frac12\int_{0}^{\pi/2}\tan(\sin^{2}x+\cos^{2}x)\,dx=\frac12\int_{0}^{\pi/2}\tan 1\,dx=\frac{\pi}{4}\tan 1.\]

## Final answer

\[\dfrac{\pi}{4}\tan 1.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q06a`. SymPy checks the addition formula for tangent and evaluates \(\tfrac12\int_{0}^{\pi/2}\tan 1\,dx\).
