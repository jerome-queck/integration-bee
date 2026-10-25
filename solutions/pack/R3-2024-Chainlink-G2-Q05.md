# R3-2024-Chainlink-G2-Q05

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 5)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 5)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 5)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/2}\frac{\sin x}{\cos x+\tan x}\,dx.
\]

## Solution

Writing the denominator over a common cosine factor produces

\[
\int_{0}^{\pi/2}\frac{\sin x\cos x}{1-\sin^{2}x+\sin x}\,dx.
\]

The substitution \(u=\sin x\) gives \(\int_{0}^{1}u/(1+u-u^{2})\,du\). The solutions PDF completes the square and evaluates the integral as \(\frac{2}{\sqrt{5}}\operatorname{artanh}(1/\sqrt{5})\).

The answers sheet also prints the logarithmic form \(\frac{1}{\sqrt{5}}\ln\frac{\sqrt{5}+1}{\sqrt{5}-1}\). The two closed forms are equal.

## Final answer

\[
\dfrac{2}{\sqrt{5}}\operatorname{artanh}\dfrac{1}{\sqrt{5}}.
\]

## SymPy self-check

SymPy integrates \(u/(1+u-u^{2})\) and evaluates the antiderivative from \(0\) to \(1\) as \(\frac{1}{\sqrt{5}}\ln\frac{\sqrt{5}+1}{\sqrt{5}-1}\). Rewriting \(\frac{2}{\sqrt{5}}\operatorname{artanh}(1/\sqrt{5})\) as a logarithm matches that value.
