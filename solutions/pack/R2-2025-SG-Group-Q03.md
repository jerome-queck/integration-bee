# R2-2025-SG-Group-Q03

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 3). The same integral is group 2 of `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK group 2)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{dx}{\sqrt[3]{\sqrt[3]{x}-x}}.
\]

## Solution

Set \(x=u^{3}\) and then \(u^{2}=v\). The integral becomes
\[
\frac32\int_{0}^{1}v^{1/3}(1-v)^{-1/3}\,dv=\frac32\,B\Bigl(\frac43,\frac23\Bigr).
\]
Reflection gives \(\Gamma(1/3)\Gamma(2/3)=2\pi/\sqrt{3}\), and \(\Gamma(4/3)=\Gamma(1/3)/3\), so the beta value is \(\pi/\sqrt{3}\). The UK mark scheme prints \(\pi/\sqrt{3}\) for this integral.

## Final answer

\[
\dfrac{\pi}{\sqrt{3}}.
\]

## SymPy self-check

SymPy rewrites \(\tfrac32\,B(4/3,2/3)\) as \(\pi/\sqrt{3}\).
