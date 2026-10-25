# R3-2024-Dichotomy-S1-Q02b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 2b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 2b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 2b)
- The catalog row is not changed.

## Problem

\[\int\frac{\tan x}{\tan(2x)}\,dx.\]

## Solution

The double-angle formula turns the integrand into \((1-\tan^{2}x)/2\). With \(\tan^{2}x=\sec^{2}x-1\), this is \((2-\sec^{2}x)/2\), whose antiderivative is \(x-\tan x/2+C\).

## Final answer

\[x-\dfrac{\tan x}{2}+C.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q02b`. SymPy checks \(\tan(2x)(1-\tan^{2}x)=2\tan x\) and differentiates \(x-\tan x/2\) back to \((1-\tan^{2}x)/2\).
