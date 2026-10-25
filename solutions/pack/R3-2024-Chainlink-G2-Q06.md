# R3-2024-Chainlink-G2-Q06

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 6)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 6)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 6)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}e^{-a^{2}x^{2}-b^{2}/x^{2}}\,dx\quad(a>0,\;b>0).
\]

## Solution

The solutions PDF scales \(x=\sqrt{b/a}\,u\). The integral becomes

\[
\sqrt{\frac{b}{a}}\int_{0}^{\infty}e^{-ab(u^{2}+1/u^{2})}\,du=\frac12\sqrt{\frac{b}{a}}\int_{-\infty}^{\infty}e^{-ab(u^{2}+1/u^{2})}\,du.
\]

That folded Gaussian is \(e^{-2ab}\) times \(\int_{-\infty}^{\infty}e^{-ab u^{2}}\,du\). The remaining Gaussian is \(\sqrt{\pi/(ab)}\), and the value is \(\sqrt{\pi}/(2a e^{2ab})\).

## Final answer

\[
\dfrac{\sqrt{\pi}}{2a\,e^{2ab}}.
\]

## SymPy self-check

SymPy checks the scaling \(x=\sqrt{b/a}\,u\) and evaluates \(\int_{-\infty}^{\infty}e^{-ab u^{2}}\,du=\sqrt{\pi/(ab)}\). Multiplying \(\sqrt{b/a}\,\sqrt{\pi/(ab)}\) by \(e^{-2ab}/2\) simplifies to \(\sqrt{\pi}/(2ae^{2ab})\). A quadrature with \(a=b=1\) matches that value within \(10^{-18}\).
