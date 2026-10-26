# R3-2024-Chainlink-G5-Q04

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, PDF page 1, problem 4.
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf`, PDF page 6, Game 5, problem 4.
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, PDF pages 18-19, Game 5, problem 4.
- Visual source check: the mark and worked solution both print \(1-\gamma-\pi^2/6\). The missing denominator in the old catalog answer was an extraction error.

## Problem

\[
\int_{0}^{1}\left(\frac{1}{x}-\left\lfloor\frac{1}{x}\right\rfloor-\frac{1}{x^{2}}\left\lfloor\frac{1}{x}\right\rfloor^{-2}\right)\,dx.
\]

## Solution

The substitution \(x=1/y\) sends the interval to \([1,\infty)\) and the integrand to

\[
\frac{1}{y}-\frac{\lfloor y\rfloor}{y^{2}}-\frac{1}{\lfloor y\rfloor^{2}}.
\]

On \([n,n+1]\) the first two terms have antiderivative \(\ln y+n/y\), and the definite piece is \(\ln(n+1)-\ln n-1/(n+1)\). Summing to \(N\) produces \(\ln(N+1)-H_{N+1}+1\), whose limit is \(1-\gamma\). The remaining terms contribute \(-\sum 1/n^{2}=-\pi^{2}/6\). The value is \(1-\gamma-\pi^{2}/6\).

## Final answer

\[
1-\gamma-\dfrac{\pi^{2}}{6}.
\]

## SymPy self-check

`verify/pack_hard_floor.py` matches the original integrand and both bounds before reducing it. SymPy checks the reciprocal Jacobian, differentiates the full interval primitive \(\ln y+n/y-y/n^2\), checks the harmonic partial-sum recurrence and its initial value, and evaluates the harmonic limit and the Basel sum.

The fractional-part term of the original integrand lies in \([0,1)\). On \((1/(n+1),1/n]\), \(1/(xn)\leq(n+1)/n\leq2\), so the other term is bounded by 4. Thus the improper endpoint is integrable, and the convergent interval sums give the original integral.
