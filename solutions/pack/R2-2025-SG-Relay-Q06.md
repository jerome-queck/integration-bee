# R2-2025-SG-Relay-Q06

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 6). The same integral is relay 6 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 6)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int\frac{f^{-1}(x)}{1+f(x)}\,dx,
\]
where \(f(x)=x^{\varphi}\) and \(\varphi=(1+\sqrt{5})/2\).

## Solution

Since \(\varphi-1=1/\varphi\), the inverse on \(x>0\) is \(x^{\varphi-1}\). The substitution \(u=x^{\varphi}\) gives
\[
\frac{1}{\varphi}\ln|1+x^{\varphi}|+C.
\]
The UK mark scheme prints that antiderivative and allows the absolute-value bars to be dropped.

## Final answer

\[
\dfrac{1}{\varphi}\ln|1+x^{\varphi}|+C.
\]

## SymPy self-check

With \(\varphi=(1+\sqrt{5})/2\), SymPy simplifies \(\varphi-1-1/\varphi\) to \(0\), and differentiates \(\ln(1+x^{\varphi})/\varphi\) back to \(x^{\varphi-1}/(1+x^{\varphi})\) for \(x>0\).
