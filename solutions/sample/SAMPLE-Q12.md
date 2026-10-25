# SAMPLE-Q12

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 12)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 12)
- Catalog row `SAMPLE-Q12` is `verify: sympy`.

## Problem

\[
\int \frac{\sqrt{\tan x}}{\sin 2x}\,dx.
\]

## Solution

The solutions PDF differentiates the printed answer:

\[
\frac{d}{dx}\sqrt{\tan x}=\frac{\sec^2 x}{2\sqrt{\tan x}}=\frac{\sqrt{\tan x}}{\sin 2x}.
\]

## Final answer

\[
\sqrt{\tan x}+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the stored antiderivative through the pack gate and recovers \(\sqrt{\tan x}/\sin 2x\).
