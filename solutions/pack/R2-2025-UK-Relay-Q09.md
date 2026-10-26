# R2-2025-UK-Relay-Q09

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (p. 3, relay 9)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (p. 3, relay 9)
- Worked source: derived in this note; the mark scheme prints the final value.

## Problem

\[
\int_{0}^{\infty}\frac{\sin x}{x(\cosh x+\cos x)}\,dx.
\]

## Solution

For \(x>0\), set \(w=\exp((-1+i)x)\). Then \(|w|=e^{-x}<1\) and

\[
\frac{\sin x}{\cosh x+\cos x}=\operatorname{Im}\frac{2w}{1+w}=2\sum_{n\geq 1}(-1)^{n-1}e^{-nx}\sin(nx).
\]

The same expansion with \(w\) replaced by \(rw\), for a fixed \(r\in(0,1)\), converges absolutely. Term-by-term integration is legitimate because \(\int_{0}^{\infty}e^{-nx}|\sin(nx)|/x\,dx\) is at most \(1\) and \(\sum r^{n}\) converges. Each integral equals \(\pi/4\), and

\[
\sum_{n\geq 1}(-1)^{n-1}r^{n}=\frac{r}{1+r},
\]

so the damped integral equals \((\pi/2)\,r/(1+r)\).

As \(r\to 1^{-}\), the damped integrand tends pointwise to the printed integrand. On \((0,\pi/2)\) its absolute value is at most \(2|\sin x|/x\leq 2\), because the denominator \(1+2re^{-x}\cos x+r^{2}e^{-2x}\) is at least \(1\). On \([\pi/2,\infty)\) it is bounded by a constant multiple of \(e^{-x}\). Dominated convergence passes the limit inside the integral, and the value tends to \(\pi/4\). The mark scheme prints \(\pi/4\).

## Final answer

\[
\frac{\pi}{4}.
\]

## SymPy self-check

The pack-gate certificate checks the imaginary-part identity, the finite
geometric-sum recurrence and its vanishing remainder, the exact Laplace
integral \(\int_0^\infty e^{-ax}\sin(ax)/x\,dx=\pi/4\), and the
limit of the integrated Abel kernel. It also verifies the algebra of the
uniform denominator bound and finiteness of the tail majorant used for
dominated convergence.
