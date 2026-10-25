# R2-2025-UK-Relay-Q15

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 15)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 15)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{1-x}{(1+x)\sqrt{x+x^{2}+x^{3}}}\,dx.
\]

## Solution

Set \(x=(1-u)/(1+u)\). Then \(u\) runs from \(1\) to \(0\) and \(dx=-2\,du/(1+u)^{2}\). The integrand pulls back to
\[
-\frac{2u}{\sqrt{1-u^{2}}\sqrt{u^{2}+3}}.
\]
Reversing the limits and setting \(w=u^{2}\) produces
\[
\int_{0}^{1}\frac{dw}{\sqrt{(1-w)(w+3)}}.
\]
The radicand is \(3-2w-w^{2}=4-(w+1)^{2}\). With the shift \(u=w+1\),
\[
\int_{1}^{2}\frac{du}{\sqrt{4-u^{2}}}=\arcsin 1-\arcsin\frac12=\frac{\pi}{2}-\frac{\pi}{6}=\frac{\pi}{3}.
\]
The mark scheme prints \(\pi/3\).

## Final answer

\[
\frac{\pi}{3}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q15`. SymPy pulls the integrand back under \(x=(1-u)/(1+u)\), checks the completed-square identities, differentiates \(\arcsin(u/2)\), and checks \(\arcsin 1-\arcsin(1/2)=\pi/3\).
