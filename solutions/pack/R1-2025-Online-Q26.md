# R1-2025-Online-Q26

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 26)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 26)
- The catalog row is not changed.

## Problem

\[
\int_0^1\frac{x(x-1)}{(x+1)\ln x}\,dx.
\]

## Solution

Expand \(1/(1+x)=\sum_{n\ge 0}(-1)^n x^n\) on \((0,1)\) and substitute \(x=e^{-t}\). Each term becomes a Frullani integral:
\[
\sum_{n=0}^\infty(-1)^n\int_0^\infty\frac{e^{-(n+2)t}(1-e^{-t})}{t}\,dt=\sum_{n=0}^\infty(-1)^n\ln\Bigl(\frac{n+3}{n+2}\Bigr).
\]
The solutions PDF pairs this alternating sum into the Wallis product for \(4/\pi\), so the sum of logarithms is \(\ln(4/\pi)\). The mark scheme prints \(\ln(4/\pi)\).

## Final answer

\[
\ln\frac4\pi.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q26`. SymPy checks \(\int_0^1 x^s\,dx=1/(s+1)\) and the Frullani evaluation \(\int_{n+1}^{n+2}dt/(t+1)=\ln((n+3)/(n+2))\). The Wallis limit of \((2M+1)!^2\pi/(2^{4M}(M!)^4(M+1))\) is \(1\). A quadrature of the original integrand matches \(\ln(4/\pi)\).
