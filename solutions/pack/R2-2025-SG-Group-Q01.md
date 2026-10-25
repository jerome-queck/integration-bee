# R2-2025-SG-Group-Q01

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 1)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{\ln(\arcsin x)}{\sqrt{(1-x^{2})\arcsin x}}\,dx.
\]

## Solution

Set \(x=\sin u\), so \(u\) runs from \(0\) to \(\pi/2\) and \(dx=\cos u\,du\). The factor \(\sqrt{1-x^{2}}=\cos u\) cancels, and the integral becomes
\[
\int_{0}^{\pi/2}\frac{\ln u}{\sqrt{u}}\,du.
\]
Put \(t=\sqrt{u}\). Then \(du=2t\,dt\) and
\[
\int_{0}^{\sqrt{\pi/2}}4\ln t\,dt=4\bigl[t\ln t-t\bigr]_{0}^{\sqrt{\pi/2}}.
\]
The limit \(t\ln t\to 0\) at the origin leaves
\[
4\sqrt{\frac{\pi}{2}}\Bigl(\frac12\ln\frac{\pi}{2}-1\Bigr)=\sqrt{2\pi}\Bigl(\ln\frac{\pi}{2}-2\Bigr).
\]

## Final answer

\[
\sqrt{2\pi}\Bigl(\ln\frac{\pi}{2}-2\Bigr).
\]

## SymPy self-check

SymPy evaluates \(4\bigl(t\ln t-t\bigr)\) at \(t=\sqrt{\pi/2}\), using \(t\ln t\to 0\) at \(0\), and simplifies the result to \(\sqrt{2\pi}(\ln(\pi/2)-2)\).
