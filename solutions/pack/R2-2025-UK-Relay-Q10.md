# R2-2025-UK-Relay-Q10

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 10)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 10)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row remains `manual` pending discrete multiplicative grading support.

## Problem

\[
\prod_{x}(2025x+2026),
\]

## Solution

where the product is the inverse of \(g(f)=f(x+1)/f(x)\). The gamma recurrence \(\Gamma(w+1)=w\Gamma(w)\) gives two equivalent discrete multiplicative antiderivatives. With \(w=x+1/2025\),
\[
\Gamma\Bigl(x+\frac{2026}{2025}\Bigr)=\Bigl(x+\frac{1}{2025}\Bigr)\Gamma\Bigl(x+\frac{1}{2025}\Bigr),
\]
and
\[
\frac{2025^{x+1}\Gamma(x+1+2026/2025)}{2025^{x}\Gamma(x+2026/2025)}=2025x+2026.
\]
The same ratio holds for \(2025^{x}(x+1/2025)\Gamma(x+1/2025)\). The mark scheme prints both
\[
C\cdot 2025^{x}\Gamma\Bigl(x+\frac{2026}{2025}\Bigr)
\quad\text{and}\quad
C\cdot 2025^{x}\Bigl(x+\frac{1}{2025}\Bigr)\Gamma\Bigl(x+\frac{1}{2025}\Bigr).
\]

The mark scheme, page 3, places \(x\) outside the fraction: the Gamma argument is \(x+2026/2025\). The earlier transcription \((x+2026)/2025\) was incorrect.

The recurrence above is proved. The current automatic grader only supports ordinary integral constants: it would accept an additive shift and reject a valid constant multiple here. A separate kind-aware grading change is needed before this row can safely become `sympy`.

## Final answer

\[
C\cdot 2025^{x}\Gamma\Bigl(x+\dfrac{2026}{2025}\Bigr)
=
C\cdot 2025^{x}\Bigl(x+\dfrac{1}{2025}\Bigr)\Gamma\Bigl(x+\dfrac{1}{2025}\Bigr).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q10`. SymPy checks \(\Gamma(w+1)=w\Gamma(w)\) and both shifts that reproduce \(2025x+2026\).
