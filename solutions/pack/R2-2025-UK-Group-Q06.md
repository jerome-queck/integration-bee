# R2-2025-UK-Group-Q06

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`, page 2, Group 6.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf`, page 2, Group 6: \(\pi\).
- Worked source: derived below; the mark scheme supplies the final value.
- Source correction: the previous catalog answer \(\phi^{-1}\log|1+x^\phi|+C\) belongs to **Relay 6 on page 3**, not Group 6. The group final is unambiguously \(\pi\).
- The same integral is SG Group 7 in `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf`, page 2.

## Problem

\[
I=\int_{-\infty}^{\infty}
\frac{\cos^2 x}{\cos^2 x+(x\cos x+\sin x+1)^2}\,dx.
\]

The isolated points where the displayed fraction is \(0/0\) have removable
extensions and do not affect the integral.

## Solution

Dividing by \(\cos^2x\) where it is nonzero reveals
\[
f(x)=\frac1{1+(x+\tan(x/2+\pi/4))^2}.
\]
A useful complex function is therefore
\[
F(z)=\frac1{z+i+\tan(z/2+\pi/4)}
    =\frac{1+i e^{iz}}{z+2i+i z e^{iz}}.
\]
The second expression defines \(F\) across poles of the tangent. For real
\(x\), direct algebra gives \(f(x)=-\operatorname{Im}F(x)\).

### Analyticity on the closed upper half plane

Write \(z=x+iy\), with \(x,y\) real and \(y\ge0\). Since
\(\lvert e^{iz}\rvert=e^{-y}\),
\[
\begin{aligned}
|z+2i|^2-|i z e^{iz}|^2
&=(x^2+y^2)(1-e^{-2y})+4y+4\\
&>0.
\end{aligned}
\]
Thus the two terms in the denominator cannot cancel. Its denominator has
no zeros on or above the real axis, so \(F\) is holomorphic there. In
particular, \(-\operatorname{Im}F\) supplies the removable real extensions
of the original integrand.

### A contour with a uniform error bound

Let \(R=2\pi N\), where \(N\) is a positive integer. Close the real segment
from \(-R\) to \(R\) with the three sides
\[
R\longrightarrow R+iR\longrightarrow -R+iR\longrightarrow -R.
\]
Call these three sides \(\Gamma_R\). They have total length \(4R\), and
\(|z|\ge R\) on all of them. Put
\[
A(z)=\frac{2i}{1+i e^{iz}},\qquad F(z)=\frac1{z+A(z)}.
\]
On either vertical side, \(e^{iz}=e^{-y}\) because
\(e^{\pm iR}=1\). Therefore
\[
|A(z)|^2=\frac4{1+e^{-2y}}\le4.
\]
On the top side, \(|e^{iz}|=e^{-R}\le e^{-2\pi}<1/3\), and the reverse
triangle inequality gives
\[
|A(z)|\le\frac2{1-e^{-R}}\le3.
\]
Consequently, on all three sides,
\[
\left|F(z)-\frac1z\right|
=\left|\frac{-A(z)}{z(z+A(z))}\right|
\le\frac3{R(R-3)}.
\]
The integral of this error has modulus at most
\[
4R\,\frac3{R(R-3)}=\frac{12}{R-3}\longrightarrow0.
\]
This proves the required uniform contour limit; pointwise asymptotics
alone would not suffice.

### Evaluating the surviving contour

Scale \(z=Rw\). The integral of \(1/z\) over \(\Gamma_R\) is independent of
\(R\). Direct integration along the three unit sides yields
\[
\int_0^1\frac{i\,dt}{1+it}
+\int_1^{-1}\frac{dt}{t+i}
+\int_1^0\frac{i\,dt}{-1+it}
=i\pi.
\]
Cauchy's theorem and the established error bound imply
\[
\lim_{N\to\infty}\int_{-2\pi N}^{2\pi N}F(x)\,dx=-i\pi.
\]
Taking minus the imaginary part gives
\(\lim_N\int_{-2\pi N}^{2\pi N}f(x)\,dx=\pi\). Since \(f\ge0\), this
finite increasing limit proves convergence of both nonnegative tails and
is the ordinary improper integral, not merely a principal value.

## Final answer

\[
\boxed{I=\pi}.
\]

## SymPy self-check

The `tangent_ray_value` proof builder, reached through `pack_gate.proven`,
keeps the original cosine-square ratio and the original limits. Its
certificate verifies the real-boundary identity, the strictly positive
no-pole norm gap, the exponential modulus, the vertical-side bound, the
top-side bound, the exact error identity, and the zero limit of the
integrated error. SymPy evaluates the three rational contour integrals
above and supplies their imaginary part as the value. Cauchy's theorem
and the nonnegative-integrand convergence argument are the analytic
justification for those checked identities. No quadrature is used as a
proof.

The builder only matches this integrand on \((-\infty,\infty)\). Changed
limits, a multiplied integrand, or a changed argument do not match. The
gate must also reject a changed final such as \(\pi+1\).
