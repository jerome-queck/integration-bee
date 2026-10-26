# R2-2025-SG-Relay-Q03

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (PDF page 1, Problem 3).
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (PDF page 3, Relay Round 3).
- Matching UK problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (PDF page 1, Problem 3). Both PDFs print the same question.
- Worked source: derived in [the UK Relay 3 note](R2-2025-UK-Relay-Q03.md), including the Fourier cancellation and the proof of every polynomial norm.

## Problem and printed answer

For positive integers \(m,n\), evaluate
\[
\int_{-1}^{1} f_n(x)f_m(x)\,dx,
\qquad
f_n(x)=\sum_{k=0}^{n+2025}
\left(x+\sqrt{x^2-1}\cos\frac{2\pi k}{n+2026}\right)^{n+26}.
\]
The mark scheme prints the complete answer
\[
\begin{cases}
\displaystyle\frac{2(n+2026)^2}{2n+53},&m=n,\\[4pt]
0,&m\ne n.
\end{cases}
\]
Both branches are required.

## Solution

Put \(d=n+26\) and \(N=n+2026\). Expanding the summand into Fourier modes
produces only integer frequencies \(h\) with \(|h|\le d<N\).
The finite roots-of-unity sum kills every nonzero frequency, leaving
\[
f_n(x)=N H_d(x),\qquad
H_d(x)=\sum_{j=0}^{\lfloor d/2\rfloor}
\binom d{2j}\binom{2j}{j}
\frac{x^{d-2j}(x^2-1)^j}{4^j}.
\]
Only even powers of the square root survive, so \(H_d\) is a real polynomial.
The imaginary square root on \((-1,1)\) requires no change to the question.

The generating function
\[
\sum_{d\ge0}H_d(x)t^d=(1-2xt+t^2)^{-1/2}
\]
gives the Legendre differential equation and three-term recurrence.
The differential equation and the vanishing endpoint factor \(1-x^2\)
give orthogonality for different nonnegative degrees. The recurrence gives
\[
\frac d{2d-1}h_d=\frac d{2d+1}h_{d-1},
\qquad
h_0=2,\qquad
h_d=\int_{-1}^1H_d(x)^2\,dx,
\]
hence \(h_d=2/(2d+1)\). Multiplying by the grid factors and substituting
\(d=n+26\) gives both printed branches. The linked UK note proves each
step for all nonnegative degrees.

## SymPy self-check

This row uses the same `legendre_grid_value` certificate through
`pack_gate.proven` as UK Relay 3. The encoding retains the original two
finite `Sum` expressions and explicit positive-integer assumptions.
The checker verifies the geometric-sum algebra, generating-series
recurrences, differential identities, Green identity, endpoint factors,
and diagonal norm recurrence. The source note explains how these checked
identities compose into the evaluation.

The integration limits, summation bounds, non-aliasing condition, radical,
parameter assumptions, and both answer branches have mutation controls.
No finite set of sample degrees supplies the proof.
