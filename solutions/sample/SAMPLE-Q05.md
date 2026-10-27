# SAMPLE-Q05

- Problem: `sources/Integration_Competition_Sample_problems.pdf`, p. 1, question 5
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`, p. 1, answer 5
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf`, p. 6, question 5

## Status: resolved symbolic certificate

Catalog row `SAMPLE-Q05` is `verify: sympy`. The gate certifies the shift and rational form of the reflection below within the existing proof timeout. The derived answer agrees with both the printed answer and the worked source.

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

All logarithm arguments are positive: on \([0,\pi/4]\), \(1+\tan t\in[1,2]\) and \(2/(1+\tan t)\in[1,2]\). Thus the logarithm subtraction uses the real logarithm without a branch ambiguity. The substitutions have nonsingular positive Jacobians on these compact intervals.

## Final answer

\[
\frac{\pi\ln 2}{8}.
\]

## SymPy self-check

`verify/sample_certificates.py` supplies the exact reflection certificate through `pack_gate.proven`. After checking \(u=x-1\), it uses the equivalent rational reflection \(u\mapsto(1-u)/(1+u)\). The certificate verifies reversed endpoints, the Jacobian-weight identity, and the logarithm sum \(\ln2\), then computes \(\int_0^1du/(1+u^2)=\pi/4\) before dividing by two. Numerical integration is not the acceptance criterion.

`solutions/sample_self_check.py` reproves the stored row and runs `check_q05`. Its additional quadrature is a sanity check. The gate must reject the wrong answers \(0\), \(\pi/4\), and \((\pi\ln 2)/4\).
