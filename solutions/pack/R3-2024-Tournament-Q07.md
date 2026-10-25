# R3-2024-Tournament-Q07

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 3, problem 7, slide 38)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 40)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.3, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{-1}^{1}\frac{2025+e^{x}+e^{-x}}{1+2025^{x}}\,dx.
\]

## Solution

The solutions PDF uses the even/odd identity

\[
\int_{-a}^{a}\frac{e(x)}{1+b^{o(x)}}\,dx=\int_{0}^{a}e(x)\,dx
\]

with \(e(x)=2025+e^{x}+e^{-x}\) even and \(o(x)=x\) odd. The integral collapses to

\[
\int_{0}^{1}(2025+e^{x}+e^{-x})\,dx=\bigl[2025x+e^{x}-e^{-x}\bigr]_{0}^{1}=2025+e-\frac{1}{e}.
\]

The answer slide prints \(2025+e-1/e\).

## Final answer

\[
2025+e-\dfrac{1}{e}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q07`. SymPy differentiates \(2025x+e^{x}-e^{-x}\) and evaluates it from \(0\) to \(1\).
