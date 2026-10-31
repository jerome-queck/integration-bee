# SAMPLE-Q14

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 14)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 14)
- Catalog row `SAMPLE-Q14` is `verify: sympy`.

## Problem

\[
\int \frac{dx}{x\bigl(1+\sin^2(\ln x)\bigr)}.
\]

## Solution

The solutions PDF sets \(u=\ln x\), so \(du=dx/x\), and the integral becomes

\[
\int \frac{du}{1+\sin^2 u}=\int \frac{\sec^2 u}{1+2\tan^2 u}\,du.
\]

A further substitution \(v=\tan u\) gives

\[
\int \frac{dv}{1+2v^2}=\frac{1}{\sqrt{2}}\arctan(\sqrt{2}\,v).
\]

That formula is valid on each interval between consecutive odd multiples of \(\pi/2\) in \(u\). At each of those points it jumps by \(-\pi/\sqrt{2}\). The integrand in \(u\) is positive and integrates to \(\pi/\sqrt{2}\) over every period of length \(\pi\). Adding \((\pi/\sqrt{2})\lfloor u/\pi+1/2\rfloor\) removes the jump. Restoring \(u=\ln x\) gives the continuous primitive. The answers PDF prints the formula without that step.

## Final answer

\[
\frac{1}{\sqrt{2}}\arctan\bigl(\sqrt{2}\tan(\ln x)\bigr)+\frac{\pi}{\sqrt{2}}\left\lfloor\frac{\ln x}{\pi}+\frac12\right\rfloor.
\]

## SymPy self-check

`verify/piecewise_primitive.py` differentiates the smooth piece by the ordinary derivative test and checks the joins at \(x=\exp((k+1/2)\pi)\).
