# R2-2025-UK-Group-Q09

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`, PDF page 2, group 9.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf`, PDF page 2, group 9.
- Worked source: derived in this note; the mark scheme prints the final value.
- Both pages were visually checked. The mark is \(\ln 2-1\). The old catalog text \(\pi/4\) is the answer to **relay** question 9 on PDF page 3; it is a row-alignment error, not a disagreement with the group problem.

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

### Why the stored Sum can pass through the integral

The transcript retains the exact logarithmic summands, with the sum inside the integral. This needs justification because the integrated series converges conditionally. For \(0<x<1\), write \(t=-\ln x>0\), and set
\[
b_n(x)=\ln\frac{1-e^{-t/n}}{1-e^{-t/(n+1)}},\qquad
c_n=\ln\frac{n+1}{n},\qquad
g(t)=\ln\frac{1-e^{-t}}t.
\]
The function \(g\) decreases on \((0,\infty)\), since
\[
g'(t)=\frac{1}{e^t-1}-\frac1t
=-\frac{e^t-1-t}{t(e^t-1)}<0.
\]
Consequently
\[
0\leq c_n-b_n(x)=g\!\left(\frac{t}{n+1}\right)-g\!\left(\frac tn\right).
\]
The beta calculation above gives \(\int_0^1 b_n(x)\,dx=1/(n+1)\). Hence the nonnegative remainder has summable integral:
\[
\sum_{n=1}^\infty\int_0^1(c_n-b_n(x))\,dx
=\lim_{N\to\infty}\left(\ln(N+1)-H_{N+1}+1\right)
=1-\gamma<\infty.
\]
Here \(H_m=\sum_{j=1}^m1/j\) and \(\gamma\) is Euler's constant. The series \(\sum(-1)^nc_n\) converges by the alternating-series test. The series of remainders converges absolutely in \(L^1(0,1)\), so its sum may be integrated term by term. Combining these two parts proves
\[
\int_0^1\sum_{n=1}^\infty(-1)^nb_n(x)\,dx
=\sum_{n=1}^\infty\int_0^1(-1)^nb_n(x)\,dx.
\]

## Final answer

\[
\ln 2-1.
\]

## SymPy self-check

`verify/pack_hard_series.py` checks the positive-power substitution, the beta derivative, the digamma recurrence, the logarithmic factorization and monotonicity identities used above, the remainder-mass recurrence and limit, and the alternating harmonic tail. Only the exact printed Sum with bounds \([0,1]\) is admitted. Changed summands, truncated sums, changed integration bounds, and a collision between the integration variable and the summation index are rejected by the matcher.
