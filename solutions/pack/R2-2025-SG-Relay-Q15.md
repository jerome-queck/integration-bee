# R2-2025-SG-Relay-Q15

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 15)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\lim_{n\to\infty}\int_{0}^{1}\sin\Biggl(\frac{\pi}{2n}\lfloor nx+1\rfloor\Biggr)\,dx.
\]

## Solution

On the interval \(((k-1)/n,k/n)\) for \(k=1,\ldots,n\), the floor \(\lfloor nx+1\rfloor\) equals \(k\). The integral is the Riemann sum
\[
\frac1n\sum_{k=1}^{n}\sin\Bigl(\frac{\pi k}{2n}\Bigr),
\]
which converges to
\[
\int_{0}^{1}\sin\Bigl(\frac{\pi x}{2}\Bigr)\,dx=\frac{2}{\pi}.
\]

## Final answer

\[
\dfrac{2}{\pi}.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{1}\sin(\pi x/2)\,dx=2/\pi\).
