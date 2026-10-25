# R2-2025-UK-Relay-Q04

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 4)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 4)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\int_{0}^{\infty}\sin(x^{2}+y^{2})\,dx\,dy.
\]

## Solution

In polar coordinates \(x=r\cos\theta\), \(y=r\sin\theta\), the first quadrant is \(\theta\in[0,\pi/2]\) and \(r\in[0,\infty)\), with area element \(r\,dr\,d\theta\). The integral is improper. Insert the damping \(e^{-\varepsilon r^{2}}\) for \(\varepsilon>0\) and let \(\varepsilon\downarrow 0\):
\[
\int_{0}^{\pi/2}\int_{0}^{\infty}e^{-\varepsilon r^{2}}\sin(r^{2})\,r\,dr\,d\theta=\frac{\pi}{2}\cdot\frac12\int_{0}^{\infty}e^{-\varepsilon u}\sin u\,du,
\]
where \(u=r^{2}\). The inner Laplace transform equals \(1/(1+\varepsilon^{2})\). The damped integral is
\[
\frac{\pi}{4}\cdot\frac{1}{1+\varepsilon^{2}},
\]
and the limit \(\varepsilon\downarrow 0\) is \(\pi/4\).

## Final answer

\[
\dfrac{\pi}{4}.
\]

## SymPy self-check

For \(\varepsilon>0\), SymPy evaluates \(\int_{0}^{\infty}e^{-\varepsilon u}\sin u\,du=1/(\varepsilon^{2}+1)\). The limit of \((\pi/4)/(1+\varepsilon^{2})\) as \(\varepsilon\to 0\) is \(\pi/4\).
