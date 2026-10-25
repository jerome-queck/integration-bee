# R3-2024-Tournament-Q05-v8

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 2, problem 5, answer slide 127)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 127)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.2, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 127, not the integral. Slide 127 is the answer reveal for Battle 3, Fight 2, problem 5:

\[
\int_{\pi/4}^{\pi/2}(\sin x)^{\tan x}\bigl(\sec^{2}x\cdot\ln(\sin x)+1\bigr)\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q05-v6`.

## Solution

The integrand is the derivative of \((\sin x)^{\tan x}\). Indeed, if \(y=\exp(\tan x\cdot\ln(\sin x))\), then

\[
\frac{y'}{y}=\sec^{2}x\cdot\ln(\sin x)+1.
\]

At the lower limit, \(y(\pi/4)=(\sqrt{2}/2)^{1}=\sqrt{2}/2\). As \(x\to(\pi/2)^{-}\), \(\tan x\to\infty\) and \(\ln(\sin x)\to 0\), and the limit of \(y\) is \(1\). The definite integral is

\[
1-\frac{\sqrt{2}}{2}.
\]

The answer slide prints \(1-\sqrt{2}/2\).

## Final answer

\[
1-\dfrac{\sqrt{2}}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q05_v8`. That check runs `check_r3_2024_tournament_q05_v6` for `R3-2024-Tournament-Q05-v6`. SymPy checks the logarithmic derivative, the value \(\sqrt{2}/2\) at \(x=\pi/4\), and the limit \(1\) as \(x\to(\pi/2)^{-}\).
