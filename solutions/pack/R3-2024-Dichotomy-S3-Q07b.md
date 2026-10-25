# R3-2024-Dichotomy-S3-Q07b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 7b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 7b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 7b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\frac{\ln\bigl(\sqrt{x}+\sqrt{1-x}\bigr)}{\sqrt{x}}\,dx.\]

## Solution

Again \(x=\sin^{2}u\). King's rule rewrites the integral as \(\int_{0}^{\pi/2}(\sin u+\cos u)\ln(\sin u+\cos u)\,du\). The shift \(u-\pi/4\) produces \[\sqrt{2}\int_{-\pi/4}^{\pi/4}\cos u\ln(\sqrt{2}\cos u)\,du.\]

The solutions PDF integrates by parts and substitutes \(y=\sin u\). The value is \(2\sqrt{2}\ln(\sqrt{2}+1)-2\).

## Final answer

\[2\sqrt{2}\ln(\sqrt{2}+1)-2.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q07b`. SymPy checks the parts derivative, evaluates \(\int_{0}^{1/\sqrt{2}} y^{2}/(1-y^{2})\,dy\), and simplifies the result to the printed value.
