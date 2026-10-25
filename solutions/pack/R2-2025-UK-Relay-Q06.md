# R2-2025-UK-Relay-Q06

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 6)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 6)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int\frac{f^{-1}(x)}{1+f(x)}\,dx,
\]
where \(f(x)=x^{\varphi}\) and \(\varphi=(1+\sqrt{5})/2\) is the golden ratio.

## Solution

The golden ratio satisfies \(\varphi-1=1/\varphi\), so the inverse is \(f^{-1}(x)=x^{\varphi-1}\) for \(x>0\). The integral is
\[
\int\frac{x^{\varphi-1}}{1+x^{\varphi}}\,dx.
\]
Set \(u=x^{\varphi}\). Then \(du=\varphi x^{\varphi-1}\,dx\), and the integral becomes
\[
\frac{1}{\varphi}\ln|1+x^{\varphi}|+C.
\]
The mark scheme prints that antiderivative and notes that the absolute-value bars may be omitted.

## Final answer

\[
\dfrac{1}{\varphi}\ln|1+x^{\varphi}|+C.
\]

## SymPy self-check

With \(\varphi=(1+\sqrt{5})/2\), SymPy simplifies \(\varphi-1-1/\varphi\) to \(0\), and differentiates \(\ln(1+x^{\varphi})/\varphi\) back to \(x^{\varphi-1}/(1+x^{\varphi})\) for \(x>0\).
