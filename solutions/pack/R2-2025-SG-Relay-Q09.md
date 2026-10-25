# R2-2025-SG-Relay-Q09

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 9)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{e}^{2e^{2}}\frac{e^{W(x)}}{x^{2}}\,dx,
\]
where \(W\) is the Lambert \(W\) function, the inverse of \(u\mapsto ue^{u}\).

## Solution

Set \(x=ue^{u}\), so \(W(x)=u\) and \(dx=e^{u}(u+1)\,du\). The endpoint \(x=e\) forces \(u=1\), and \(x=2e^{2}\) forces \(u=2\). Substituting,
\[
\frac{e^{u}}{(ue^{u})^{2}}\cdot e^{u}(u+1)\,du=\Bigl(\frac1u+\frac{1}{u^{2}}\Bigr)\,du.
\]
Therefore
\[
\int_{1}^{2}\Bigl(\frac1u+\frac{1}{u^{2}}\Bigr)\,du=\ln 2+\frac12.
\]

## Final answer

\[
\ln 2+\dfrac{1}{2}.
\]

## SymPy self-check

With \(x=ue^{u}\), SymPy simplifies \(e^{u}/x^{2}\cdot dx/du-(1/u+1/u^{2})\) to \(0\), and evaluates \(\int_{1}^{2}(1/u+1/u^{2})\,du=\ln 2+1/2\).
