# R3-2024-Dichotomy-S1-Q05a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 5a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 5a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 5a)
- The catalog row is not changed.

## Problem

\[\int_{e^{2}}^{e^{e}}\frac{\ln\bigl(x^{(\ln\ln x)^{2}}/\ln x\bigr)}{(\ln\ln x)^{3}\ln x}\,dx.\]

## Solution

The numerator of the integrand is \((\ln\ln x)^{2}\ln x-\ln(\ln x)\). Dividing by the printed denominator leaves the derivative of \(x/\ln(\ln x)\). The solutions PDF evaluates that antiderivative from \(e^{2}\) to \(e^{e}\): \[\frac{e^{e}}{\ln(\ln e^{e})}-\frac{e^{2}}{\ln(\ln e^{2})}=e^{e}-\frac{e^{2}}{\ln 2}.\]

## Final answer

\[e^{e}-\dfrac{e^{2}}{\ln 2}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q05a`. SymPy differentiates \(x/\ln(\ln x)\) back to the integrand and evaluates the endpoints.
