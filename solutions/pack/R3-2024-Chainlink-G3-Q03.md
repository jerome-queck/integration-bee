# R3-2024-Chainlink-G3-Q03

- Problem: `sources/past/r3/2024/Chainlink_Game_3_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 3)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 3, problem 3)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 3, problem 3)
- The catalog row is not changed.

## Problem

\[
\int\bigl(x+2x^{2}+\cdots+2025 x^{2025}\bigr)\bigl(1+x+\cdots+x^{2024}\bigr)\,dx.
\]

## Solution

Write \(s=x+x^{2}+\cdots+x^{2025}\). Then \(s'=1+2x+\cdots+2025 x^{2024}\), and

\[
\bigl(x+2x^{2}+\cdots+2025 x^{2025}\bigr)\bigl(1+x+\cdots+x^{2024}\bigr)=s\,s'.
\]

The antiderivative is \(s^{2}/2+C\). The finite geometric sum \(s=(x-x^{2026})/(1-x)\) gives the second form printed on the answers sheet.

## Final answer

\[
\dfrac12\bigl(x+x^{2}+\cdots+x^{2025}\bigr)^{2}+C.
\]

## SymPy self-check

For \(x\neq 1\) and a positive integer \(n\), SymPy sums \(\sum_{j=0}^{n-1}x^{j}\) to \((1-x^{n})/(1-x)\) and \(\sum_{k=1}^{n}kx^{k}\) to \(x s'\), where \(s=x(1-x^{n})/(1-x)\). The product of those sums is \(s s'\), and the derivative of \(s^{2}/2\) is the same product. At \(n=2025\), \(s=(x-x^{2026})/(1-x)\).
