# R3-2024-Tournament-Q03-v3

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 1, problem 3, answer slide 18)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 18)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.1, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 18, not the integral. Slide 18 is the answer reveal for Battle 1, Fight 1, problem 3:

\[
\int_{0}^{\pi/2}\frac{2-\sqrt{\tan x}+\tan x}{1+\tan^{3/2}x}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q03`.

## Solution

King's substitution \(x\mapsto \pi/2-x\) replaces \(\tan x\) by \(\cot x\). Clearing the resulting powers of \(\cot x\) produces the partner

\[
\int_{0}^{\pi/2}\frac{2\tan^{3/2}x-\tan x+\sqrt{\tan x}}{1+\tan^{3/2}x}\,dx.
\]

The average of the two numerators is \(2(1+\tan^{3/2}x)\), so the average integrand is \(1\). Therefore

\[
I=\frac12\int_{0}^{\pi/2}1\,dx=\frac{\pi}{2}.
\]

The answer slide prints \(\pi/2\).

## Final answer

\[
\dfrac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q03_v3`. That check runs `check_r3_2024_tournament_q03` for `R3-2024-Tournament-Q03`. SymPy checks that the reflected numerator is \(2t^{3/2}-t+\sqrt{t}\) and that the two numerators sum to twice the denominator.
