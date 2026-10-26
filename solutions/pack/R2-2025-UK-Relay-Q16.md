# R2-2025-UK-Relay-Q16

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (PDF page 5, relay 16)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (PDF page 4, relay 16)
- Worked source: derived in this note; the mark scheme prints the final value.

## Problem

\[
\int_{\sqrt{2}-1}^{\sqrt{2}+1}\frac{dx}{x\bigl(e+(x^{2}+1)^{1/\ln x}\bigr)}.
\]

## Solution

Set \(x=e^{t}\). The limits are \(\pm\ln(1+\sqrt{2})\), because \((\sqrt{2}-1)(\sqrt{2}+1)=1\). Write
\[
A(t)=\exp\bigl(\ln(e^{2t}+1)/t\bigr).
\]
Then \(A(-t)=e^{2}/A(t)\), and
\[
\frac{1}{e+A(t)}+\frac{1}{e+e^{2}/A(t)}=\frac{1}{e}.
\]
The integrand in \(t\) is the first term. Folding the symmetric interval multiplies the constant \(1/e\) by the half-length, and the integral is \((\ln(1+\sqrt{2}))/e\). The mark scheme prints \((1/e)\ln(\sqrt{2}+1)\).

## Final answer

\[
\dfrac{1}{e}\ln(1+\sqrt{2}).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q16`. SymPy checks \(A(-t)=e^{2}/A(t)\), the constant sum \(1/e\), and the reciprocal endpoints.

The pack gate checks the positive logarithm branches under \(x\mapsto1/x\), the reciprocal endpoints, and the reflected sum \(1/(ex)\). Since the transformed factor is between \(0\) and \(1/e\), the undefined point \(x=1\) does not cause divergence.
