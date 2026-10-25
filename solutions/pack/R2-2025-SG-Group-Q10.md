# R2-2025-SG-Group-Q10

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 10)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{x(2x+3)(x+1)^{1/3}}{x^{6}+x^{2}+2x+1}\,dx.
\]

## Solution

The denominator is \(x^{6}+(x+1)^{2}\). Set \(u=(x+1)/x^{3}\). Then \(du=-(2x+3)/x^{4}\,dx\) and \((x+1)^{1/3}=u^{1/3}x\), so

\[
\frac{x(2x+3)(x+1)^{1/3}}{x^{6}+(x+1)^{2}}\,dx=-\frac{u^{1/3}}{1+u^{2}}\,du.
\]

As \(x\) runs from \(0^{+}\) to \(\infty\), \(u\) runs from \(\infty\) to \(0\). The two sign changes cancel and the integral is

\[
\int_{0}^{\infty}\frac{u^{1/3}}{1+u^{2}}\,du.
\]

The substitution \(v=u^{2}\) gives

\[
\frac12\int_{0}^{\infty}\frac{v^{2/3-1}}{1+v}\,dv=\frac12\cdot\frac{\pi}{\sin(2\pi/3)}=\frac{\pi}{\sqrt{3}},
\]

by the standard formula \(\int_{0}^{\infty}v^{a-1}/(1+v)\,dv=\pi/\sin(\pi a)\) at \(a=2/3\).

## Final answer

\[
\frac{\pi}{\sqrt{3}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_group_q10`. SymPy checks the derivative of \(u\), the rewritten denominator, the Jacobian algebra, and the beta evaluation.
