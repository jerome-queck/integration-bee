# R2-2025-SG-Relay-Q12

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (PDF page 3, relay 12)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.

## Problem

\[
\int_{3}^{7}\frac{10-\{x\}}{\lfloor x\rfloor+\lfloor 10-x\rfloor+10}\,dx,
\]
where \(\{x\}\) is the fractional part.

## Solution

On each interval \((n,n+1)\) with \(n\in\{3,4,5,6\}\), one has \(\lfloor x\rfloor=n\) and \(\lfloor 10-x\rfloor=9-n\), so the denominator is \(n+(9-n)+10=19\). The numerator is \(10-(x-n)=10+n-x\). Each piece is
\[
\int_{n}^{n+1}\frac{10+n-x}{19}\,dx=\frac12.
\]
Four such intervals give \(2\). The integers themselves do not affect the integral.

## Final answer

\[
2.
\]

## SymPy self-check

SymPy evaluates \(\int_{n}^{n+1}(10+n-x)/19\,dx=1/2\). Four copies sum to \(2\).

The pack gate checks the strict inequalities defining each open unit block and integrates the resulting linear piece exactly. Integer endpoints form a finite set and do not affect the result.
