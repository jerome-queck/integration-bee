# SAMPLE-Q05

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 5)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 5)
- Catalog row `SAMPLE-Q05` stays `verify: manual`. The pack gate does not finish the original integral inside its time limit.

## Problem

\[
\int_1^2 \frac{\ln x}{x^2-2x+2}\,dx.
\]

## Solution

The solutions PDF completes the square, \(x^2-2x+2=(x-1)^2+1\), and sets \(u=x-1\):

\[
I=\int_0^1 \frac{\ln(u+1)}{u^2+1}\,du.
\]

The substitution \(u=\tan\theta\) gives

\[
I=\int_0^{\pi/4}\ln(1+\tan\theta)\,d\theta.
\]

Reflection \(t=\pi/4-\theta\) uses \(\tan(\pi/4-t)=(1-\tan t)/(1+\tan t)\), so

\[
I=\int_0^{\pi/4}\ln\left(\frac{2}{1+\tan t}\right)\,dt=\frac{\pi}{4}\ln 2-I.
\]

Therefore \(2I=(\pi/4)\ln 2\) and \(I=(\pi\ln 2)/8\).

## Final answer

\[
\frac{\pi\ln 2}{8}.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs `check_q05`. SymPy simplifies \(\tan(\pi/4-t)-(1-\tan t)/(1+\tan t)\) to \(0\), and then \(\ln(1+(1-\tan t)/(1+\tan t))-\ln(2/(1+\tan t))\) to \(0\). A quadrature of the original integrand on \([1,2]\) matches \((\pi\ln 2)/8\) within \(10^{-12}\).
