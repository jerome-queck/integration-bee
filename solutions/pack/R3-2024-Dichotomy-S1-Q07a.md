# R3-2024-Dichotomy-S1-Q07a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 7a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 7a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 7a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\frac{1}{(1+x^{2})\bigl(1+\pi/2+\arctan x\operatorname{arccot} x\bigr)}\,dx.\]

## Solution

Since \(\arctan x+\operatorname{arccot} x=\pi/2\), the second factor is \((1+\arctan x)(1+\operatorname{arccot} x)\). The solutions PDF splits the integrand into the two reciprocal factors, substitutes \(u=\arctan x\), and obtains \[\frac{1}{2+\pi/2}\int_{0}^{\pi/4}\left(\frac{1}{1+\pi/2-u}+\frac{1}{1+u}\right)du=\frac{1}{2+\pi/2}\ln\Bigl(1+\frac{\pi}{2}\Bigr).\]

## Final answer

\[\dfrac{1}{2+\pi/2}\ln\Bigl(1+\dfrac{\pi}{2}\Bigr).\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q07a`. SymPy checks that \(\arctan x+\operatorname{arccot} x\) is constant and equals \(\pi/2\) at \(x=1\), and that the evaluated logarithm is \(\ln(1+\pi/2)/(2+\pi/2)\).
