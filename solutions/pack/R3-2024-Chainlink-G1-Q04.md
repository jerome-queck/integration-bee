# R3-2024-Chainlink-G1-Q04

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 4)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 4)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 4)
- The catalog row is not changed.

## Problem

\[
\int_{1}^{\infty}\frac{1}{x\sqrt{x}\sqrt{x-1}}\,dx.
\]

## Solution

The solutions PDF sets \(u=\sqrt{x}\). Then \(x=u^{2}\) and the integral becomes

\[
\int_{1}^{\infty}\frac{2}{u^{2}\sqrt{u^{2}-1}}\,du.
\]

The domain \((1,\infty)\) allows \(u=\sec t\), with \(t\) running from \(0\) to \(\pi/2\). On that interval \(\sqrt{\sec^{2}t-1}=\tan t\), and the integrand collapses to \(2\cos t\). The value is \(2\).

## Final answer

\[
2.
\]

## SymPy self-check

SymPy simplifies the substitution \(x=u^{2}\) to \(2/(u^{2}\sqrt{u^{2}-1})\). With \(\sqrt{\sec^{2}t-1}\) replaced by \(\tan t\) for \(t\in(0,\pi/2)\), the secant substitution simplifies to \(2\cos t\), whose integral from \(0\) to \(\pi/2\) is \(2\).
