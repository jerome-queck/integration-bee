# R2-2025-SG-Group-Q14

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 14)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int\frac{(x+1)^{2}+(3x+1)\sqrt{x+\ln x}}{x\sqrt{x+\ln x}\,\bigl(x+\sqrt{x+\ln x}\bigr)}\,dx,
\]
on the interval where \(x+\ln x>0\).

## Solution

Set \(t=\sqrt{x+\ln x}\). Differentiating \(2t+2\ln|x+t|\) produces the integrand. The antiderivative is
\[
2\sqrt{x+\ln x}+2\ln\bigl|x+\sqrt{x+\ln x}\bigr|+C.
\]

## Final answer

\[
2\sqrt{x+\ln x}+2\ln\bigl|x+\sqrt{x+\ln x}\bigr|+C.
\]

## SymPy self-check

With \(t=\sqrt{x+\ln x}\), SymPy simplifies the difference between the derivative of \(2t+2\ln(x+t)\) and the integrand to \(0\) for \(x>0\).
