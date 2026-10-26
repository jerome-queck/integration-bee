# R3-2024-Chainlink-G2-Q07

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 7)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 7)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 7)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[
\int_{0}^{\pi/2}\frac{\cos^{3}x\sin x}{\ln(\sin x)}\,dx.
\]

## Solution

Set \(u=\sin x\). Then \(\cos^{2}x=1-u^{2}\) and the integral is \(\int_{0}^{1}(1-u^{2})u/\ln u\,du\). The further substitution \(y=u^{2}\) produces

\[
\int_{0}^{1}\frac{1-y}{\ln y}\,dy.
\]

The solutions PDF differentiates in a parameter: \(I(a)=\int_{0}^{1}(1-y^{a})/\ln y\,dy\) has \(I'(a)=-1/(a+1)\) and \(I(0)=0\), so \(I(a)=-\ln(a+1)\). The needed value is \(I(1)=-\ln 2\).

## Final answer

\[
-\ln 2.
\]

## SymPy self-check

The gate checks the sine substitution and the power-parameter identity, including its negative sign. The positive inner kernel justifies the order of integration and gives the printed value.
