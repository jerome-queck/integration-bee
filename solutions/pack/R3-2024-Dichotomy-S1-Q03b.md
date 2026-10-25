# R3-2024-Dichotomy-S1-Q03b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 3b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 3b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 3b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{1}{1+(\sqrt{x})^{e}}\,dx.\]

## Solution

Again \(u=\sqrt{x}\), so the integral is \(\int_{0}^{\infty} 2u/(1+u^{e})\,du\). The further substitution \(u=y^{1/e}\) produces \[\frac{2}{e}\int_{0}^{\infty}\frac{y^{2/e-1}}{1+y}\,dy=\frac{2}{e}\,\mathrm{B}\Bigl(\frac{2}{e},1-\frac{2}{e}\Bigr)=\frac{2\pi}{e}\csc\frac{2\pi}{e}.\]

## Final answer

\[\dfrac{2\pi}{e}\csc\dfrac{2\pi}{e}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q03b`. SymPy checks the Jacobian of \(u=y^{1/e}\) and the reflection \(\Gamma(z)\Gamma(1-z)=\pi/\sin(\pi z)\).
