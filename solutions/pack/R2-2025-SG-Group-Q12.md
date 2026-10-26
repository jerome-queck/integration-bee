# R2-2025-SG-Group-Q12

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf`, PDF page 2, group 12. The same series of integrals is group 9 on PDF page 2 of `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf`, PDF page 2, UK group 9. This is the UK mark for the identical question, not a separate Singapore mark scheme.
- Worked source: derived in this note.
- All three pages were visually checked. Both problem sheets print the same series, and the UK group mark is \(\ln 2-1\).

## Problem

\[
\sum_{n=1}^{\infty}\int_{0}^{1}(-1)^{n}\ln\Bigl(\frac{1-x^{1/n}}{1-x^{1/(n+1)}}\Bigr)\,dx.
\]

## Solution

The beta function \(B(n,s)=\Gamma(n)\Gamma(s)/\Gamma(n+s)\) satisfies \(B(n,1)=1/n\), and
\[
\frac{\partial B}{\partial s}=B\bigl(\psi(s)-\psi(n+s)\bigr).
\]
At \(s=1\) this derivative is \(-H_{n}/n\), because \(\psi(n+1)+\gamma=H_{n}\). The substitution \(x=v^{n}\) therefore gives
\[
\int_{0}^{1}\ln(1-x^{1/n})\,dx=-H_{n}.
\]
The difference of the two logarithms integrates to \(H_{n+1}-H_{n}=1/(n+1)\). The series is
\[
\sum_{n\ge 1}\frac{(-1)^{n}}{n+1}=\ln 2-1.
\]
The mark scheme prints \(\ln 2-1\).

The stored transcript keeps the logarithmic summands as a `Sum` inside the integral. The justification for exchanging their order is given in `solutions/pack/R2-2025-UK-Group-Q09.md`: with \(b_n(x)\) the positive logarithm above and \(c_n=\ln((n+1)/n)\), one has \(c_n-b_n\geq0\) and
\[
\sum_{n=1}^\infty\int_0^1(c_n-b_n(x))\,dx=1-\gamma<\infty.
\]
The alternating constants \(\sum(-1)^nc_n\) converge, and the remainder is absolutely summable in \(L^1\). Thus the transcript and the printed series of integrals have the same value.

## Final answer

\[
\ln 2-1.
\]

## SymPy self-check

`verify/pack_hard_series.py` checks the same substitution, beta derivative, digamma recurrence, absolutely summable remainder, and alternating harmonic tail as UK group 9. The certificate matches the exact Sum and its \([0,1]\) bounds before doing any symbolic work.
