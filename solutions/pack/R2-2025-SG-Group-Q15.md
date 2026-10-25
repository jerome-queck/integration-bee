# R2-2025-SG-Group-Q15

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 15)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\sum_{n=1}^{\infty}x^{n}\lim_{t\to 0}\frac{d^{n-1}}{dt^{n-1}}\left(\frac{t^{n}}{n!\,\sin^{n}t}\right)dx.
\]

## Solution

The function \(h(t)=(t/\sin t)^{n}/n!\) is analytic at the origin. The limit in the sum is \((n-1)!\) times the coefficient of \(t^{n-1}\) in \(h\), which is

\[
\frac{1}{n}\,[t^{n-1}]\Bigl(\frac{t}{\sin t}\Bigr)^{n}.
\]

That coefficient is also the coefficient of \(x^{n}\) in \(\arcsin x\). Indeed, on a small circle about the origin,

\[
[x^{n}]\arcsin x=\frac{1}{2\pi i}\oint\frac{\arcsin x}{x^{n+1}}\,dx.
\]

The substitution \(x=\sin t\) is conformal near \(0\), and \(\arcsin(\sin t)=t\) on the image contour, so the integral becomes

\[
\frac{1}{2\pi i}\oint\frac{t\cos t}{\sin^{n+1}t}\,dt.
\]

The identity \(\cos t/\sin^{n+1}t=-(1/n)\,d/dt(\sin^{-n}t)\) and integration by parts on the closed contour, where \(t\sin^{-n}t\) is single-valued and meromorphic, give

\[
[x^{n}]\arcsin x=\frac{1}{n}\,[t^{n-1}]\Bigl(\frac{t}{\sin t}\Bigr)^{n}.
\]

The series of \(\arcsin x\) has nonnegative coefficients, so the sum inside the integral is \(\arcsin x\) on \([0,1]\). Then

\[
\int_{0}^{1}\arcsin x\,dx=\bigl[x\arcsin x+\sqrt{1-x^{2}}\bigr]_{0}^{1}=\frac{\pi}{2}-1.
\]

## Final answer

\[
\frac{\pi}{2}-1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_group_q15`. SymPy checks the derivative identity for \(\sin^{-n}t\), matches the arcsine coefficients through degree \(8\), and evaluates the antiderivative on \([0,1]\).
