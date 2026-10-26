# R3-2024-Dichotomy-S2-Q06a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (PDF p. 3, problem 6a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (PDF p. 5, Segment 2, problem 6a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (PDF p. 11, Segment 2, problem 6a)
- The catalog gate checks the trigonometric split and logarithmic scaling. The answer PDF includes the factor \(1/2\) omitted by the old catalog extraction.

## Problem

\[\int_{0}^{\infty}\frac{\cos x-\cos^{2}x}{x^{2}}\ln x\,dx.\]

## Solution

The solutions PDF writes \(\cos x-\cos^{2}x=\sin^{2}x-2\sin^{2}(x/2)\). After the substitution \(x=2u\) in the second piece, the integral is \[\int_{0}^{\infty}\frac{\sin^{2}x}{x^{2}}\ln x\,dx-\int_{0}^{\infty}\frac{\sin^{2}x}{x^{2}}\ln(2x)\,dx=-\ln 2\int_{0}^{\infty}\frac{\sin^{2}x}{x^{2}}\,dx=-\frac{\pi\ln 2}{2}.\]

## Final answer

\[-\dfrac{\pi\ln 2}{2}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q06a`. SymPy evaluates \(\int_{0}^{\infty}\sin^{2}x/x^{2}\,dx=\pi/2\).
