# R2-2025-SG-Relay-Q29

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 29). The same product is relay 10 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 10)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\prod_{x}(2025x+2026).
\]

## Solution

where the product is the inverse of \(g(f)=f(x+1)/f(x)\). The gamma recurrence \(\Gamma(w+1)=w\Gamma(w)\) gives two equivalent antiderivatives. With \(w=x+1/2025\),
\[
\Gamma\Bigl(x+\frac{2026}{2025}\Bigr)=\Bigl(x+\frac{1}{2025}\Bigr)\Gamma\Bigl(x+\frac{1}{2025}\Bigr),
\]
and
\[
\frac{2025^{x+1}\Gamma(x+1+2026/2025)}{2025^{x}\Gamma(x+2026/2025)}=2025x+2026.
\]
The same ratio holds for \(2025^{x}(x+1/2025)\Gamma(x+1/2025)\). The mark scheme prints both
\[
C\cdot 2025^{x}\Gamma\Bigl(\frac{x+2026}{2025}\Bigr)
\quad\text{and}\quad
C\cdot 2025^{x}\Bigl(x+\frac{1}{2025}\Bigr)\Gamma\Bigl(x+\frac{1}{2025}\Bigr).
\]

## Final answer

\[
C\cdot 2025^{x}\Gamma\Bigl(\dfrac{x+2026}{2025}\Bigr)
=
C\cdot 2025^{x}\Bigl(x+\dfrac{1}{2025}\Bigr)\Gamma\Bigl(x+\dfrac{1}{2025}\Bigr).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q29`. SymPy checks the same gamma recurrence as the UK relay 10 note.
