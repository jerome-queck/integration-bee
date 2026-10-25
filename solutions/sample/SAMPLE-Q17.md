# SAMPLE-Q17

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 17)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 17)
- Catalog row `SAMPLE-Q17` is `verify: sympy`.

## Problem

\[
\int x^{1/\ln x}\,dx.
\]

## Solution

The solutions PDF writes \(x=e^{\ln x}\), so \(x^a=e^{a\ln x}\). Then

\[
x^{1/\ln x}=e^{(\ln x)/\ln x}=e.
\]

The integral of the constant \(e\) is \(ex+C\). The answers sheet prints `ex + c` on one baseline. That is the product \(e\cdot x\), not \(e^x\).

## Final answer

\[
ex+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` simplifies \(x^{1/\ln x}\) to \(e\) and differentiates \(ex\) through the pack gate. It rejects both \(e^x\) and \(\ln|\ln x|\) as antiderivatives of this integrand.
