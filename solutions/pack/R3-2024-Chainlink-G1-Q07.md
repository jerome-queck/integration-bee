# R3-2024-Chainlink-G1-Q07

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 7)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 7)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 7)
- The catalog row is not changed.

## Problem

\[
\int_{\arctan(1/3)}^{\arctan(1/2)}\frac{x}{\sin(4x)}\,dx.
\]

## Solution

The addition formula gives \(\arctan(1/3)+\arctan(1/2)=\pi/4\). The substitution \(y=4x\) therefore runs between two limits that add to \(\pi\). Reflecting one copy of \(\int y/\sin y\,dy\) across \(y\mapsto\pi-y\) replaces the factor \(y\) by \(\pi/2\), and

\[
\int\frac{1}{\sin y}\,dy=\ln|\csc y-\cot y|.
\]

The solutions PDF simplifies the resulting logarithm with \(\cos(4\arctan(1/2))=-7/25\), and the value is \(\frac{\pi}{16}\ln(4/3)\).

The answers sheet also prints the unevaluated logarithm in \(\csc\) and \(\cot\), and the two forms

\[
\frac{\pi}{32}\ln\frac{1-\cos(4\arctan(1/2))}{1+\cos(4\arctan(1/2))},\qquad\frac{\pi}{32}\ln\frac{1+\cos(4\arctan(1/3))}{1-\cos(4\arctan(1/3))}.
\]

The solutions PDF carries every one of those expressions to \(\frac{\pi}{16}\ln(4/3)\).

## Final answer

\[
\dfrac{\pi}{16}\ln\dfrac{4}{3}.
\]

## SymPy self-check

SymPy checks \(\tan(\arctan(1/2)+\arctan(1/3))=1\). The derivative of \(\ln(\csc y-\cot y)\) is \(\csc y\). The double-angle polynomial \(8\cos^{4}\theta-8\cos^{2}\theta+1\) at \(\cos\theta=2/\sqrt{5}\) equals \(-7/25\), and \(\frac{\pi}{32}\ln((1+7/25)/(1-7/25))\) simplifies to \(\frac{\pi}{16}\ln(4/3)\).
