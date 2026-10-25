# R1-2025-Online-Q16

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 16)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 16)
- The catalog row is not changed.

## Problem

\[
\int_0^\infty\frac{1}{(x^4+1)^2}\,dx.
\]

## Solution

The solutions PDF starts from the two equal integrals
\[
J=\int_0^\infty\frac{1}{x^4+1}\,dx=\int_0^\infty\frac{x^2}{x^4+1}\,dx=\int_0^\infty\frac{1}{x^2+2}\,dx=\frac{\pi}{2\sqrt{2}}.
\]
Writing \(1=(1+x^4)-x^4\) gives
\[
\int_0^\infty\frac{1}{(x^4+1)^2}\,dx=\int_0^\infty\left(\frac{1}{x^4+1}-\frac{x^4}{(x^4+1)^2}\right)\,dx.
\]
Integration by parts on the second term, with boundary contribution \(x/(4(x^4+1))\) vanishing at both ends, produces \(\frac34 J\):
\[
\frac34\cdot\frac{\pi}{2\sqrt{2}}=\frac{3\pi}{8\sqrt{2}}.
\]
This equals \(3\sqrt{2}\,\pi/16\). The mark scheme prints \(3\pi/(8\sqrt{2})\).

## Final answer

\[
\frac{3\pi}{8\sqrt{2}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q16`. SymPy checks \(1/(x^4+1)-x^4/(x^4+1)^2=1/(x^4+1)^2\) and the derivative of the boundary term \(x/(4(x^4+1))\). It evaluates \(\int_0^\infty(1+x^2)/(1+x^4)\,dx=\pi/\sqrt{2}\) and takes \(\frac38\) of that value.
