# R3-2024-Chainlink-G2-Q02

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 2)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 2)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 2)
- The catalog row is not changed.

## Problem

\[
\int e^{e^{e^{x}}}\,e^{e^{x}}\,e^{e^{x}}\,e^{x}\,dx.
\]

## Solution

Set \(u=e^{e^{x}}\). Then \(u'=e^{e^{x}}e^{x}\) and \(e^{u}=e^{e^{e^{x}}}\), so the integrand is \(u\,e^{u}\,u'\). Integration by parts gives

\[
\int u e^{u}\,du=ue^{u}-e^{u}+C=e^{e^{e^{x}}}(e^{e^{x}}-1)+C.
\]

## Final answer

\[
e^{e^{e^{x}}}\bigl(e^{e^{x}}-1\bigr)+C.
\]

## SymPy self-check

SymPy differentiates \(e^{e^{e^{x}}}(e^{e^{x}}-1)\) back to \(e^{e^{e^{x}}}e^{e^{x}}e^{e^{x}}e^{x}\).
