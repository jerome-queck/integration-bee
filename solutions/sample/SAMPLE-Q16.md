# SAMPLE-Q16

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 16)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 16)
- Catalog row `SAMPLE-Q16` is `verify: sympy`.

## Problem

\[
\int \frac{dx}{2+\sin x}.
\]

## Solution

The solutions PDF uses the Weierstrass substitution \(t=\tan(x/2)\), so \(\sin x=2t/(1+t^2)\) and \(dx=2\,dt/(1+t^2)\). The integral becomes

\[
\int \frac{dt}{(t+1/2)^2+3/4}=\frac{2}{\sqrt{3}}\arctan\left(\frac{2t+1}{\sqrt{3}}\right).
\]

The substitution is valid on each interval between consecutive odd multiples of \(\pi\). At each of those points the printed formula jumps by \(-2\pi/\sqrt{3}\). The integrand is continuous and positive, and its integral over a period of length \(2\pi\) is \(2\pi/\sqrt{3}\). Adding \((2\pi/\sqrt{3})\lfloor(x+\pi)/(2\pi)\rfloor\) removes the jump. The answers PDF prints the formula without that step.

## Final answer

\[
\frac{2}{\sqrt{3}}\arctan\left(\frac{2\tan(x/2)+1}{\sqrt{3}}\right)+\frac{2\pi}{\sqrt{3}}\left\lfloor\frac{x}{2\pi}+\frac12\right\rfloor.
\]

## SymPy self-check

`verify/piecewise_primitive.py` differentiates the smooth piece by the ordinary derivative test and checks the joins at odd multiples of \(\pi\).
