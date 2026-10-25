# R3-2024-Dichotomy-S1-Q04b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 4b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 4b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 4b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1/2}\left(\frac{x}{\sqrt{x+\dfrac{x}{\sqrt{x+\cdots}}}}+\sqrt{x^{3}+x^{2}\sqrt{x^{3}+x^{2}\sqrt{\cdots}}}\right)dx.\]

## Solution

Write \(f(x)\) for the first continued radical and \(g(x)\) for the second. Then \(f^{3}+f^{2}x-x^{2}=0\) and \(g^{2}-x^{2}g-x^{3}=0\). Swapping the variables turns one cubic into the other, so \(f\) and \(g\) are inverse functions. The solutions PDF records \(g(0)=0\) and \(g(1/2)=1/2\), and the integral of a function plus its inverse on that interval is \((1/2)\cdot(1/2)=1/4\).

## Final answer

\[\dfrac{1}{4}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q04b`. SymPy checks that the two cubics match after the variables are swapped, that \(g(1/2)=1/2\) satisfies the equation for \(g\), and that \((1/2)^{2}=1/4\).
