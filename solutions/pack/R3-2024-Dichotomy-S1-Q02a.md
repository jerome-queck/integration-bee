# R3-2024-Dichotomy-S1-Q02a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 2a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 2a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 2a)
- The catalog row is not changed.

## Problem

\[\int\frac{\tan(2x)}{\tan x}\,dx.\]

## Solution

From \(\tan(2x)=2\tan x/(1-\tan^{2}x)\), the integrand is \(2/(1-\tan^{2}x)\). The substitution \(u=\tan x\) produces \[\int\frac{2}{(1-u^{2})(1+u^{2})}\,du=\frac12\ln\left|\frac{1+u}{1-u}\right|+\arctan u+C.\]

Back in \(x\), that is the first printed antiderivative. The answers sheet also prints \(x-\tfrac12\bigl(\ln|\cos x-\sin x|-\ln|\cos x+\sin x|\bigr)\) and \(\operatorname{artanh}(\tan x)+x+C\).

## Final answer

\[\dfrac12\bigl(\ln|1+\tan x|-\ln|1-\tan x|\bigr)+x+C.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q02a`. SymPy differentiates the substituted antiderivative back to \(2/(1-\tan^{2}x)\). The three printed expressions have the same derivative, and the logarithmic form of \(\operatorname{artanh} u\) matches \(\tfrac12\ln((1+u)/(1-u))\).
