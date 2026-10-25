# R3-2024-Tournament-Q02

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 1, problem 2, slide 11)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 13)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.1, problem 2)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/4}(4\cos^{2}x-1)\sqrt{\tan x}\,dx.
\]

## Solution

The solutions PDF starts from \(4\cos^{2}x-1=2\cos(2x)+1\). Integration by parts on the cosine piece uses

\[
\frac{d}{dx}\bigl(\sin(2x)\sqrt{\tan x}\bigr)=2\cos(2x)\sqrt{\tan x}+\sin(2x)\frac{\sec^{2}x}{2\sqrt{\tan x}}.
\]

The boundary term is \(1\) at \(x=\pi/4\) and \(0\) at \(x=0\), so

\[
\int_{0}^{\pi/4}2\cos(2x)\sqrt{\tan x}\,dx=1-\int_{0}^{\pi/4}\frac{\sin(2x)\sec^{2}x}{2\sqrt{\tan x}}\,dx.
\]

The substitution \(t=\tan x\) turns that remainder into \(\int_{0}^{1}\sqrt{t}/(1+t^{2})\,dt\). The same substitution turns \(\int_{0}^{\pi/4}\sqrt{\tan x}\,dx\) into the same integral. Those two pieces cancel, and the original integral equals \(1\). The answer slide prints \(1\).

## Final answer

\[
1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q02`. SymPy checks \(4\cos^{2}x-1=2\cos(2x)+1\), the \(t=\tan x\) form of the remainder, and the boundary values \(0\) and \(1\).
