# R2-2025-SG-Group-Q07

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf`, page 2, Group 7.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf`, page 2, **UK Group 6**: \(\pi\).
- Matching UK problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`, page 2, Group 6. These two printed integrals are identical; the SG question has a different number.
- Worked source: derived in [the UK Group 6 note](R2-2025-UK-Group-Q06.md), including every contour bound and the convergence argument.

## Problem

\[
I=\int_{-\infty}^{\infty}
\frac{\cos^2x}{\cos^2x+(x\cos x+\sin x+1)^2}\,dx.
\]

## Solution

Set
\[
F(z)=\frac{1+i e^{iz}}{z+2i+i z e^{iz}}.
\]
On the real axis the integrand is \(-\operatorname{Im}F(x)\). For
\(z=x+iy\), \(y\ge0\),
\[
|z+2i|^2-|iz e^{iz}|^2
=(x^2+y^2)(1-e^{-2y})+4y+4>0,
\]
so \(F\) has no pole in the closed upper half plane.

Close \([-R,R]\) by a rectangle of height \(R\), taking \(R=2\pi N\).
On its remaining three sides write
\(F(z)=1/(z+A(z))\), where \(A(z)=2i/(1+i e^{iz})\).
The vertical sides satisfy \(|A|\le2\); the top satisfies \(|A|\le3\).
Since \(|z|\ge R\) there and the three sides have total length \(4R\),
\[
\left|\int_{\Gamma_R}\left(F(z)-\frac1z\right)\,dz\right|
\le\frac{12}{R-3}\longrightarrow0.
\]
The three sides have \(\int_{\Gamma_R}dz/z=i\pi\). Cauchy's theorem gives
\(\int_{-R}^R F(x)\,dx\to-i\pi\), hence \(I=\pi\).
Nonnegativity of the original integrand makes this the ordinary
improper integral. Its isolated undefined values have removable
extensions and do not change the result.

## Final answer

\[
\boxed{I=\pi}.
\]

## SymPy self-check

This row uses the same `tangent_ray_value` certificate through
`pack_gate.proven` as UK Group 6. It checks the original ratio against
\(-\operatorname{Im}F\), the no-pole gap, both contour bounds, the
vanishing error, and the three exact rational contour integrals.
Cauchy's theorem applies because the checked gap is strictly positive;
nonnegativity supplies improper convergence. The full derivation and
mutation guards are recorded in the linked UK note.
