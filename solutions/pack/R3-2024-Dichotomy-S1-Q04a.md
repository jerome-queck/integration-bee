# R3-2024-Dichotomy-S1-Q04a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 4a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 4a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 4a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\sqrt{x^{2}\sqrt{2^{-x}\sqrt{x^{4}\sqrt{4^{-x}\sqrt{x^{8}\sqrt{8^{-x}\cdots}}}}}}}\,dx.\]

## Solution

The solutions PDF expands the nested radical, leaving a convergence limit to the reader, and obtains \(x^{2}\,2^{-(4/9)x}\). The exponent of \(2\) is \(-x\sum_{m\ge 1}m/4^{m}=- (4/9)x\). The resulting gamma integral is \[\int_{0}^{\infty}x^{2}2^{-(4/9)x}\,dx=\frac{9^{3}\Gamma(3)}{4^{3}(\ln 2)^{3}}=\frac{729}{32(\ln 2)^{3}}.\]

## Final answer

\[\dfrac{729}{32(\ln 2)^{3}}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q04a`. SymPy sums \(\sum_{m\ge 1}m/4^{m}=4/9\) and evaluates the gamma integral as \(729/(32(\ln 2)^{3})\).
