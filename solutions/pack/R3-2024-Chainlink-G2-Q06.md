# R3-2024-Chainlink-G2-Q06

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 6)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 6)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 6)
- Verification: the SymPy gate checks the source transcription and its reduction.

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

The gate checks the reciprocal substitution \(x\mapsto b/(ax)\), which preserves the exponential and changes the measure by \(b/(ax^2)\). Averaging the two copies gives the Jacobian \((a+b/x^2)/(2a)\). The increasing substitution \(u=ax-b/x\) then ranges over the whole real line, while \(a^2x^2+b^2/x^2=u^2+2ab\). SymPy checks those identities, the endpoint limits, and the remaining full Gaussian integral for symbolic positive \(a,b\).
