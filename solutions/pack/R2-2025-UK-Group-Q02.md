# R2-2025-UK-Group-Q02

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (group 2)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (group 2)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{dx}{\sqrt[3]{\sqrt[3]{x}-x}}.
\]

## Solution

Set \(x=u^{3}\). Then \(dx=3u^{2}\,du\) and
\[
\sqrt[3]{x}-x=u(1-u^{2}),
\]
so the integral becomes
\[
\int_{0}^{1}\frac{3u^{5/3}}{(1-u^{2})^{1/3}}\,du.
\]
The further substitution \(u^{2}=v\) produces
\[
\frac32\int_{0}^{1}v^{1/3}(1-v)^{-1/3}\,dv=\frac32\,B\Bigl(\frac43,\frac23\Bigr).
\]
The beta function is \(\Gamma(4/3)\Gamma(2/3)\). Using \(\Gamma(4/3)=\Gamma(1/3)/3\) and the reflection formula \(\Gamma(1/3)\Gamma(2/3)=\pi/\sin(\pi/3)=2\pi/\sqrt{3}\),
\[
\frac32\cdot\frac13\cdot\frac{2\pi}{\sqrt{3}}=\frac{\pi}{\sqrt{3}}.
\]

## Final answer

\[
\dfrac{\pi}{\sqrt{3}}.
\]

## SymPy self-check

SymPy rewrites \(\tfrac32\,B(4/3,2/3)\) as \(\pi/\sqrt{3}\).
