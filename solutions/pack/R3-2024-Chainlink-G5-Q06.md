# R3-2024-Chainlink-G5-Q06

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 6)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 6)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 6)
- The catalog row is not changed.

## Problem

\[
\int_{-\infty}^{\infty}\frac{1}{(x^{4}+1)^{2}}\,dx.
\]

## Solution

The integrand is even. The substitution \(y=x^{4}\) converts the positive half into a beta integral:

\[
\int_{-\infty}^{\infty}\frac{1}{(x^{4}+1)^{2}}\,dx=\frac12 B\Bigl(\frac14,\frac74\Bigr)=\frac{\Gamma(1/4)\Gamma(7/4)}{2}.
\]

Then \(\Gamma(7/4)=\frac34\Gamma(3/4)\). The duplication formula gives \(\Gamma(1/4)\Gamma(3/4)=\sqrt{2}\,\pi\), and the value is \(\dfrac{3\sqrt{2}}{8}\pi\).

## Final answer

\[
\dfrac{3\sqrt{2}}{8}\pi.
\]

## SymPy self-check

SymPy checks \(\Gamma(7/4)=\frac34\Gamma(3/4)\) and the duplication identity \(\Gamma(1/4)\Gamma(3/4)=2^{1/2}\sqrt{\pi}\,\Gamma(1/2)=\sqrt{2}\,\pi\). One half of \(B(1/4,7/4)\) is therefore \(3\sqrt{2}\,\pi/8\).
