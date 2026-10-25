# R3-2024-Tournament-Q06-v9

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 2, problem 6, slide 179)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 181)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.2, problem 3)
- The catalog row is not changed.

## Problem

\[
\int_{-\infty}^{\infty}\frac{\sin^{2}x}{45x^{2}+x^{2}\arctan x+x^{2}\sqrt{2025+(\arctan x)^{2}}}\,dx.
\]

## Solution

Write the denominator as \(x^{2}\) times \(45+\arctan x+\sqrt{45^{2}+(\arctan x)^{2}}\). For an even function \(e\), an odd function \(o\), and a constant \(b>0\),

\[
\frac{1}{b+o+\sqrt{b^{2}+o^{2}}}+\frac{1}{b-o+\sqrt{b^{2}+o^{2}}}=\frac{1}{b}.
\]

Take \(e(x)=\sin^{2}x/x^{2}\), \(o(x)=\arctan x\), and \(b=45\). Averaging the integrand with its reflection \(x\mapsto -x\) therefore replaces the rational factor by \(1/45\) and leaves

\[
I=\frac{1}{45}\int_{0}^{\infty}\frac{\sin^{2}x}{x^{2}}\,dx=\frac{1}{45}\cdot\frac{\pi}{2}=\frac{\pi}{90}.
\]

The solutions PDF reaches \(\pi/90\) by this calculation and describes the integrand as even. The numerator \(\sin^{2}x\) is even, but the factor of \(\arctan x\) in the denominator is odd, so the integrand itself is not an even function. The average with its reflection is what produces \(\pi/90\). The answer slide prints \(\pi/90\).

## Final answer

\[
\dfrac{\pi}{90}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q06_v9`. SymPy checks that the two rational factors sum to \(1/b\), evaluates \(\int_{0}^{\infty}\sin^{2}x/x^{2}\,dx=\pi/2\), and divides by \(45\).
