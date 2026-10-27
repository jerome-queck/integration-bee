# SAMPLE-Q09

- Problem: `sources/Integration_Competition_Sample_problems.pdf`, p. 1, question 9
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`, p. 1, answer 9
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf`, p. 10, question 9

## Status: resolved symbolic certificate

Catalog row `SAMPLE-Q09` is `verify: sympy`. The floor-piece certificate gives the printed final answer. One intermediate line of the worked PDF gives the lower endpoint of \(\int x^{-3}\,dx\) as \(0\); its next line evaluates from \(1\). The printed problem has lower endpoint \(1\), which is used throughout the derivation and certificate here.

## Problem

\[
\int_1^\infty \frac{x-\lfloor x\rfloor}{x^4}\,dx.
\]

## Solution

On each interval \(k\le x<k+1\) the floor is \(k\). The solutions PDF splits the integrand as \(x^{-3}-\lfloor x\rfloor x^{-4}\):

\[
\int_1^\infty x^{-3}\,dx=\frac12,
\]

and

\[
\int_1^\infty \frac{\lfloor x\rfloor}{x^4}\,dx=\sum_{k\ge 1}\int_k^{k+1}\frac{k}{x^4}\,dx.
\]

More directly, the complete integral on one unit interval is

\[
\begin{aligned}
\int_k^{k+1}\frac{x-k}{x^4}\,dx
&=\left[-\frac{1}{2x^2}+\frac{k}{3x^3}\right]_k^{k+1}\\
&=\frac16\left(\frac1{k^2}-\frac1{(k+1)^2}\right)
  -\frac1{3(k+1)^3}.
\end{aligned}
\]

The squared-reciprocal terms telescope. The remaining series is \(\zeta(3)-1\), so the total is

\[
\frac16-\frac13(\zeta(3)-1)=\frac12-\frac{\zeta(3)}3.
\]

The integral converges absolutely because \(0\le x-\lfloor x\rfloor<1\) and \(\int_1^\infty x^{-4}\,dx<\infty\). Changing the value at an integer endpoint does not affect the integral. The same bound permits taking the limit of the sums over successive unit intervals.

## Final answer

\[
\frac12-\frac{\zeta(3)}{3}.
\]

## SymPy self-check

`verify/sample_certificates.py` supplies the exact floor-sum certificate through `pack_gate.proven`. It matches the original integrand and bounds, integrates each rational piece, and evaluates the convergent series.

`solutions/sample_self_check.py` reproves the stored row and runs `check_q09`. SymPy independently sums \(\int_k^{k+1}(x-k)/x^4\,dx\) over \(k\ge1\). Wrong-answer controls reject \(0\), \(1/2+\zeta(3)/3\), and \(\zeta(3)/3\).
