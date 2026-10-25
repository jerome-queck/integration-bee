# R3-2024-Tournament-Q03-v9

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 1, problem 3, answer slide 116)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 116)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.1, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 116, not the integral. Slide 116 is the answer reveal for Battle 3, Fight 1, problem 3:

\[
\int_{0}^{\pi/2}\sin x\sqrt{\sin 2x}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q03-v7`.

## Solution

King's substitution \(x\mapsto\pi/2-x\) replaces \(\sin x\) by \(\cos x\) and leaves \(\sin 2x\) unchanged. Averaging the two copies gives

\[
I=\frac12\int_{0}^{\pi/2}(\sin x+\cos x)\sqrt{\sin 2x}\,dx.
\]

The double-angle identity \(\sin 2x=1-(\sin x-\cos x)^{2}\) and the substitution \(y=\sin x-\cos x\) then give \(dy=(\cos x+\sin x)\,dx\), with limits from \(-1\) to \(1\):

\[
I=\frac12\int_{-1}^{1}\sqrt{1-y^{2}}\,dy=\frac12\cdot\frac{\pi}{2}=\frac{\pi}{4}.
\]

The inner integral is the area of a semicircle of radius \(1\). The answer slide prints \(\pi/4\).

## Final answer

\[
\dfrac{\pi}{4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q03_v9`. That check runs `check_r3_2024_tournament_q03_v7` for `R3-2024-Tournament-Q03-v7`. SymPy checks \(\sin 2x=1-(\sin x-\cos x)^{2}\), the derivative of \(\sin x-\cos x\), and \(\int_{-1}^{1}\sqrt{1-y^{2}}\,dy=\pi/2\).
