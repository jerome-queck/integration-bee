# R3-2024-Tournament-Q09

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 3, problem 9, slide 48)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 50)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.3, problem 3)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\left(\sqrt{x+x^{3}}+\sqrt{x+\sqrt[3]{x}}\right)dx.
\]

## Solution

On the second square root set \(u^{3}=x\). Then \(dx=3u^{2}\,du\) and

\[
\int_{0}^{1}\sqrt{x+\sqrt[3]{x}}\,dx=\int_{0}^{1}3u^{2}\sqrt{u^{3}+u}\,du.
\]

Adding the first square root produces

\[
\int_{0}^{1}(1+3x^{2})\sqrt{x+x^{3}}\,dx=\left[\frac23(x+x^{3})^{3/2}\right]_{0}^{1}=\frac{4\sqrt{2}}{3}.
\]

The answer slide prints \(4\sqrt{2}/3\).

## Final answer

\[
\dfrac{4\sqrt{2}}{3}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q09`. SymPy checks the substituted sum \((1+3x^{2})\sqrt{x+x^{3}}\) and evaluates the antiderivative from \(0\) to \(1\).
