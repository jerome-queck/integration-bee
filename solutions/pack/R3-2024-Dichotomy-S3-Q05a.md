# R3-2024-Dichotomy-S3-Q05a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 5a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 5a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 5a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{\sqrt[3]{(1+3/x)^{x}}-\sqrt{(1+2/x)^{x}}}{x}\,dx.\]

## Solution

Let \(f(t)=(1+1/t)^{t}\). Then \(\sqrt[3]{(1+3/x)^{x}}=f(x/3)\) and \(\sqrt{(1+2/x)^{x}}=f(x/2)\). The solutions PDF identifies the integral as a Frullani integral. With \(f(0^{+})=1\) and \(f(\infty)=e\), \[\int_{0}^{\infty}\frac{f(x/3)-f(x/2)}{x}\,dx=(1-e)\ln\frac{3}{2}=(e-1)\ln\frac{2}{3}.\]

## Final answer

\[(e-1)\ln\dfrac{2}{3}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q05a`. SymPy checks the two root identifications, the limits of \(f\), and the logarithm identity.
