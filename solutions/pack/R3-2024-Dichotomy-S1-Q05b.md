# R3-2024-Dichotomy-S1-Q05b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 5b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 5b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 5b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\ln\bigl(x^{\ln(1-\ln x)+1-\ln x}\bigr)\,dx.\]

## Solution

The integrand is \(\bigl(\ln(1-\ln x)+1-\ln x\bigr)\ln x\). The solutions PDF substitutes \(y=\ln x\) and evaluates the resulting integrals by parts and the gamma function. The value it prints is \(-4\).

## Final answer

\[-4.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q05b`. A 25-digit quadrature of \(\bigl(\ln(1-\ln x)+1-\ln x\bigr)\ln x\) on \((0,1)\) matches \(-4\) within \(10^{-12}\).
