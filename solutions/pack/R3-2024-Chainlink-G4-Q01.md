# R3-2024-Chainlink-G4-Q01

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 1)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 1)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 1)
- The catalog row is not changed.

## Problem

\[
\int\frac{\sin^{2}x}{\cos^{4}x}\,dx.
\]

## Solution

The solutions PDF rewrites the integrand as \(\tan^{2}x\sec^{2}x\):

\[
\int\tan^{2}x\sec^{2}x\,dx=\frac{\tan^{3}x}{3}+C.
\]

## Final answer

\[
\dfrac{\tan^{3}x}{3}+C.
\]

## SymPy self-check

SymPy checks \(\sin^{2}x/\cos^{4}x=\tan^{2}x\sec^{2}x\) and differentiates \(\tan^{3}x/3\) back to that integrand.
