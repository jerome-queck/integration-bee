# R3-2024-Dichotomy-S2-Q03b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 3b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 3b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 3b)
- The catalog row is not changed.

## Problem

\[\int\frac{(x+1)^{2}}{(x+2)(x^{2}+x+1)}\,dx.\]

## Solution

The solutions PDF decomposes the integrand as \[\frac13\left(\frac{2x+1}{x^{2}+x+1}+\frac{1}{x+2}\right)\]

and integrates to \(\tfrac13\bigl(\ln(x^{2}+x+1)+\ln|x+2|\bigr)+C\). The denominator is \(1+(x+1)^{3}\), so the same antiderivative is \(\tfrac13\ln|1+(x+1)^{3}|+C\). Both forms are printed on the answers sheet.

## Final answer

\[\dfrac13\ln\bigl|1+(x+1)^{3}\bigr|+C.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q03b`. SymPy differentiates both antiderivatives back to the integrand and checks \((x+2)(x^{2}+x+1)=1+(x+1)^{3}\).
