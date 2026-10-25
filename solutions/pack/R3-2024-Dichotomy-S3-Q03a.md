# R3-2024-Dichotomy-S3-Q03a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 3a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 3a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 3a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{x^{1/3}}{1+x^{3}}\,dx.\]

## Solution

The solutions PDF quotes the beta evaluation \[\int_{0}^{\infty}\frac{x^{a}}{1+x^{b}}\,dx=\frac{\pi}{b}\csc\Bigl(\frac{a+1}{b}\pi\Bigr).\]

Here \(a=1/3\) and \(b=3\), so the value is \((\pi/3)\csc(4\pi/9)\). The answers sheet also prints \((\pi/3)\sec(\pi/18)\).

## Final answer

\[\dfrac{\pi}{3}\csc\dfrac{4\pi}{9}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q03a`. SymPy checks \(\csc(4\pi/9)=\sec(\pi/18)\).
