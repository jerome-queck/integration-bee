# R2-2025-UK-Relay-Q14

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 14)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 14)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{x^{e/2-1}(1+\ln x)}{x^{e}+1}\,dx.
\]

## Solution

For \(0<a<b\), the substitution \(x^{b}=u/(1-u)\) gives
\[
I(a)=\int_{0}^{\infty}\frac{x^{a-1}}{1+x^{b}}\,dx=\frac{1}{b}B\Bigl(\frac{a}{b},1-\frac{a}{b}\Bigr)=\frac{\pi/b}{\sin(\pi a/b)},
\]
using \(\Gamma(z)\Gamma(1-z)=\pi/\sin(\pi z)\). Here \(b=e\) and the extra factor \(1+\ln x\) is \(I(e/2)+I'(e/2)\). The closed form \((\pi/e)/\sin(\pi a/e)\) equals \(\pi/e\) at \(a=e/2\), and its derivative has a factor \(\cos(\pi a/e)\) which vanishes there. The value is \(\pi/e\). The mark scheme prints \(\pi/e\).

## Final answer

\[
\frac{\pi}{e}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q14`. SymPy checks the gamma reflection, evaluates the closed form at \(a=e/2\), and checks that its \(a\)-derivative vanishes there.
