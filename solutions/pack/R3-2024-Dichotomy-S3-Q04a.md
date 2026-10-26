# R3-2024-Dichotomy-S3-Q04a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, page 2, Problem 4a.
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, page 6, Segment 3, Problem 4a.
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, page 14.
- All three source pages were visually checked. The answer is a fraction \(G/2\); the previous catalog text `G` had lost the denominator. There is no disagreement between the original problem, mark, and worked solution.

## Problem

\[
I=\int_1^{\infty}\frac{\arctan(1/x^2)}{x}\,dx.
\]

## Solution

First set \(u=1/x\), then \(v=u^2\):
\[
I=\int_0^1\frac{\arctan(u^2)}{u}\,du
=\frac12\int_0^1\frac{\arctan v}{v}\,dv.
\]
Integrating the arctangent series gives
\[
I=\frac12\sum_{k=0}^{\infty}\frac{(-1)^k}{2k+1}
  \int_0^1v^{2k}\,dv
=\frac12\sum_{k=0}^{\infty}\frac{(-1)^k}{(2k+1)^2}
=\frac G2.
\]
The integrated absolute terms have finite sum, so this exchange of summation
and integration is valid. The worked PDF reaches the same series directly on
\([1,\infty)\).

## Final answer

\[
\boxed{\frac G2}.
\]

## SymPy certificate

`verify/pack_hard_catalan.py` checks the reciprocal substitution and endpoints,
then uses `pack_gate._atan_over_power` at power \(2\). That existing
certificate checks the power substitution, arctangent Taylor series,
individual term integrals, and Catalan sum. The transcript retains
`atan(1/x**2)/x`; it records the full printed answer `Catalan/2`.
