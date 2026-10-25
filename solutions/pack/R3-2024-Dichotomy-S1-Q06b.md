# R3-2024-Dichotomy-S1-Q06b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 6b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 6b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 6b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\pi/4}\left(\ln\frac{\cos x+\sin x}{\sqrt{2}\sin x}+\ln(\tan x)\right)dx.\]

## Solution

The first logarithm is \(\ln\bigl(\cos(\pi/4-x)/\sin x\bigr)\). Averaging it with the reflection \(x\mapsto\pi/4-x\) produces \(\int_{0}^{\pi/4}\ln(\cot x)\,dx\). Adding \(\int_{0}^{\pi/4}\ln(\tan x)\,dx\) leaves \(\int_{0}^{\pi/4}\ln 1\,dx=0\).

## Final answer

\[0.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q06b`. SymPy checks \((\cos x+\sin x)/(\sqrt{2}\sin x)=\cos(\pi/4-x)/\sin x\), that \(\tan x\cot x=1\), and that \(\int_{0}^{\pi/4}\ln 1\,dx=0\).
