# R2-2025-UK-Relay-Q03

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (PDF page 1, Problem 3).
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (PDF page 3, Relay Round 3).
- Worked source: derived in this note; the mark scheme supplies the final answer.
- Source check: the UK and SG problem PDFs print the same question.

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
Both branches are required. The square root is generally imaginary on the
integration interval. The finite sum nevertheless becomes a real polynomial;
replacing the square root by \(\sqrt{1-x^2}\) would change the problem.

## 1. The finite grid keeps only the constant Fourier coefficient

Put \(d=n+26\) and \(N=n+2026\). These are positive integers and
\(N-d=2000>0\). Expanding
\((x+s\cos\theta)^d\), with \(s^2=x^2-1\), gives Fourier modes
\(e^{ih\theta}\) with integer \(|h|\le d\). For a nonzero such mode,
\[
\sum_{k=0}^{N-1}e^{2\pi i hk/N}
=\frac{1-e^{2\pi i h}}{1-e^{2\pi i h/N}}=0.
\]
The denominator is nonzero because \(0<|h|<N\). The zero mode has sum
\(N\). Using
\(\cos\theta=(e^{i\theta}+e^{-i\theta})/2\), its coefficient in an odd
power is zero and in \(\cos^{2j}\theta\) is
\(4^{-j}\binom{2j}{j}\). Consequently
\[
f_n(x)=N H_d(x),\qquad
H_d(x)=\sum_{j=0}^{\lfloor d/2\rfloor}
\binom d{2j}\binom{2j}{j}
\frac{x^{d-2j}(x^2-1)^j}{4^j}.
\]
This also proves that \(H_d\) is a polynomial of degree at most \(d\),
independent of the chosen sign of the square root.

## 2. Identify the polynomial without testing finitely many degrees

As a power series near \(t=0\),
\[
\begin{aligned}
\sum_{d\ge0}H_d(x)t^d
&=\frac1{1-xt}\sum_{j\ge0}\binom{2j}{j}
\left(\frac{t^2(x^2-1)}{4(1-xt)^2}\right)^j\\
&=\frac1{\sqrt{(1-xt)^2-t^2(x^2-1)}}\\
&=\frac1{\sqrt{1-2xt+t^2}}=:G(x,t).
\end{aligned}
\]
The first equality uses
\(\sum_{r\ge0}\binom{r+2j}{2j}u^r=(1-u)^{-2j-1}\).
The square root is the analytic branch taking value 1 at \(t=0\).
This is the Legendre generating function, so \(H_d=P_d\). The next two
steps prove the properties needed here directly, rather than assuming
orthogonality from the name.

## 3. Derive orthogonality from a checked differential identity

Direct differentiation of \(G\) gives
\[
\frac{\partial}{\partial x}\bigl((1-x^2)G_x\bigr)
+t^2G_{tt}+2tG_t=0.
\]
Comparing the coefficient of \(t^d\) yields
\[
\bigl((1-x^2)H_d'(x)\bigr)'
+d(d+1)H_d(x)=0.
\]
Multiply the equations for degrees \(d,r\) by \(H_r,H_d\) and subtract.
Integration by parts gives
\[
[d(d+1)-r(r+1)]\int_{-1}^1H_dH_r\,dx
=\left[(1-x^2)(H_dH_r'-H_rH_d')\right]_{-1}^{1}=0.
\]
The boundary term vanishes because the functions are polynomials and
\(1-x^2=0\) at both endpoints. For different nonnegative integer degrees,
\(d(d+1)-r(r+1)=(d-r)(d+r+1)\ne0\), hence the integral is zero.

## 4. Derive the exact diagonal norm

The further identity
\[
(1-2xt+t^2)G_t=(x-t)G
\]
gives the recurrence
\[
(d+1)H_{d+1}=(2d+1)xH_d-dH_{d-1},
\qquad H_0=1,\quad H_1=x.
\]
Write \(h_d=\int_{-1}^1H_d^2\,dx\). Expand
\(\int_{-1}^1xH_{d-1}H_d\,dx\) by the recurrence in its two possible
ways and use the orthogonality just proved. For every integer \(d\ge1\),
\[
\frac d{2d-1}h_d=\frac d{2d+1}h_{d-1}.
\]
Since \(h_0=\int_{-1}^1 1\,dx=2\), induction yields
\[
h_d=\frac2{2d+1}.
\]
Finally \(f_n=(n+2026)H_{n+26}\). The degrees coincide exactly when
\(m=n\), giving the two printed branches above.

## SymPy self-check

The encoding retains the two original finite `Sum` expressions. Their
parameters are explicitly declared positive integers; the declarations must
survive serialization. The checker admits only grids whose degree is a
nonnegative integer strictly smaller than their number of points, with the
printed cosine argument, square root, summation endpoints, and integration
limits.

The certificate checks the finite geometric-sum algebra, the symbolic
coefficient recurrences for the two generating series, the generating
function algebra, both displayed differential identities, Green's
integration-by-parts identity, the endpoint factors, and the norm recurrence
with its exact base integral. These identities hold for symbolic indices;
a finite grid of sample values is not the proof. The roots-of-unity
non-aliasing argument, coefficient comparison, and integration by parts
justify how the checked identities compose into the integral evaluation.
The answer contains neither an unevaluated integral nor an unevaluated sum.
