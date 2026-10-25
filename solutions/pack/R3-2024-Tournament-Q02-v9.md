# R3-2024-Tournament-Q02-v9

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 1, problem 2, slide 158)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 160)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.1, problem 2)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}x^{3}\sin^{2}(\ln x)\cos^{2}(\ln x)\,dx.
\]

## Solution

The double-angle identity gives

\[
\sin^{2}(\ln x)\cos^{2}(\ln x)=\frac18-\frac18\cos(4\ln x).
\]

The first piece is

\[
\frac18\int_{0}^{1}x^{3}\,dx=\frac{1}{32}.
\]

For the second piece set \(x=e^{y}\), so \(y\) runs from \(-\infty\) to \(0\). The integral becomes

\[
\frac18\int_{-\infty}^{0}e^{4y}\cos(4y)\,dy.
\]

An antiderivative of \(e^{4y}\cos(4y)\) is \(e^{4y}(\cos 4y+\sin 4y)/8\). It vanishes at \(-\infty\) and equals \(1/8\) at \(y=0\), so the second piece is \(1/64\). Subtracting gives

\[
\frac{1}{32}-\frac{1}{64}=\frac{1}{64}.
\]

The solutions PDF reaches the same value by taking the real part of \(\int e^{4y(1+i)}\,dy\). The answer slide prints \(1/64\).

## Final answer

\[
\dfrac{1}{64}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q02_v9`. SymPy checks the trigonometric reduction, differentiates \(e^{4y}(\cos 4y+\sin 4y)/8\), and evaluates \(1/32-1/64\).
