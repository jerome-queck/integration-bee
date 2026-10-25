# R3-2024-Dichotomy-S3-Q02a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 2a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 2a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 2a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{1}{\sqrt{1+\sqrt{e^{x}}}}\,dx.\]

## Solution

Set \(u=\sqrt{1+\sqrt{e^{x}}}\). The solutions PDF computes \(u'=(u^{2}-1)/(4u)\), so the integral is \[\int_{\sqrt{2}}^{\infty}\frac{4}{u^{2}-1}\,du=2\bigl(\ln(\sqrt{2}+1)-\ln(\sqrt{2}-1)\bigr).\]

The answers sheet also prints \(4\operatorname{arsinh} 1\) and \(4\operatorname{artanh}(1/\sqrt{2})\).

## Final answer

\[2\bigl(\ln(\sqrt{2}+1)-\ln(\sqrt{2}-1)\bigr).\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q02a`. SymPy checks \(u'=(u^{2}-1)/(4u)\) and the agreement of the three printed closed forms.
