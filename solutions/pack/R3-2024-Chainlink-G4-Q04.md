# R3-2024-Chainlink-G4-Q04

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 4)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 4)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 4)
- The catalog row is not changed.

## Problem

\[
\int\sqrt{\frac{\ln\bigl(x+\sqrt{1+x^{2}}\bigr)}{1+x^{2}}}\,dx.
\]

## Solution

Set \(u=\ln(x+\sqrt{1+x^{2}})=\operatorname{arsinh}x\). Then \(du=dx/\sqrt{1+x^{2}}\), and the square root over the whole fraction becomes \(\sqrt{u}\,du\):

\[
\int\sqrt{u}\,du=\frac23 u^{3/2}+C=\frac23\bigl(\operatorname{arsinh}x\bigr)^{3/2}+C.
\]

The answers sheet also prints the same antiderivative with \(\operatorname{arsinh}x\) written as the logarithm.

## Final answer

\[
\dfrac{2}{3}\bigl(\operatorname{arsinh}x\bigr)^{3/2}+C.
\]

## SymPy self-check

SymPy differentiates \(\frac23(\operatorname{arsinh}x)^{3/2}\) to \(\sqrt{\operatorname{arsinh}x/(1+x^{2})}\), and checks \(\operatorname{arsinh}x=\ln(x+\sqrt{1+x^{2}})\).
