# R3-2024-Tournament-Q09-v5

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 3, problem 9, answer slide 99)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 99)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.3, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 99 prints the final value of Battle 2, Fight 3, problem 9:

\[
\int\sec x\,(\sec x+\tan x)^{2025}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q09-v4`.

## Solution

Set \(u=\sec x+\tan x\). Then

\[
u'=\sec x\tan x+\sec^{2}x=\sec x\,(\sec x+\tan x)=\sec x\cdot u.
\]

The integrand is \(u^{2024}u'\), so

\[
\int u^{2024}\,du=\frac{(\sec x+\tan x)^{2025}}{2025}+C.
\]

The answer slide prints the same antiderivative.

## Final answer

\[
\dfrac{(\sec x+\tan x)^{2025}}{2025}+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q09_v5`. That check runs `check_r3_2024_tournament_q09_v4` for `R3-2024-Tournament-Q09-v4`. SymPy checks \(u'=\sec x\cdot u\) and differentiates \(u^{2025}/2025\).
