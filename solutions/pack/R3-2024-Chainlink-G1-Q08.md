# R3-2024-Chainlink-G1-Q08

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 8)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 8)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 8)
- The catalog row is not changed.

## Problem

\[
\lim_{n\to\infty}(n+1)\int_{0}^{1}x^{x^{x}+n}\ln(1+x+x^{x}+x^{x^{x}}+x^{x^{x^{x}}})\,dx.
\]

## Solution

The solutions PDF treats the more general limit \((n+1)\int_{0}^{1}x^{n}f(x)\,dx\) for an integrable \(f\) that is continuous at \(1\), and shows that the limit is \(f(1)\). Given \(\varepsilon>0\), continuity supplies \(\delta\in(0,1)\) with \(|f-f(1)|<\varepsilon/2\) on \((1-\delta,1]\). The piece over \([0,1-\delta]\) is at most \((n+1)(1-\delta)^{n}\) times an integrable bound, which is smaller than \(\varepsilon/2\) for large \(n\). The piece over \((1-\delta,1]\) is at most \(\varepsilon/2\).

Here \(f(x)=x^{x^{x}}\ln(1+x+x^{x}+x^{x^{x}}+x^{x^{x^{x}}})\), so the integrand is \(x^{n}f(x)\). Then \(f(1)=\ln 5\).

## Final answer

\[
\ln 5.
\]

## SymPy self-check

SymPy evaluates \((n+1)\int_{0}^{1}x^{n}\,dx=1\) for \(n>0\), and \(\ln(1+1+1+1+1)=\ln 5\).
