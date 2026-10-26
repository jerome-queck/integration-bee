# R2-2025-SG-Relay-Q15

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (PDF page 4, relay 15)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The SymPy transcript retains the finite integrands under a limit; the exchange with integration is checked below.

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

The certificate also checks \(\lfloor y+1\rfloor-y=1-\{y\}\), so
\[
0<\frac{\lfloor nx+1\rfloor}{n}-x\le\frac1n.
\]
Since the derivative of sine has absolute value at most \(1\), the finite integrand differs from \(\sin(\pi x/2)\) uniformly by at most \(\pi/(2n)\). This bound tends to zero and justifies storing the literal limit under the integral over \([0,1]\). The original outer-limit question and the stored integral have the same value.
