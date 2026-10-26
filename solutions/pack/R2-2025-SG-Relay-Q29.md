# R2-2025-SG-Relay-Q29

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (p.8, relay 29). The same product is relay 10 on p.3 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (p.3, UK relay 10)
- Worked source: derived in this note.
- The catalog row is `verify: sympy`, with kind `discrete_multiplicative`.

## Problem

\[
\prod_{x}(2025x+2026).
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

Here \(C\ne0\); zero cannot be an antiderivative because its forward quotient
is undefined. The identities hold on the common domain of \(F(x)\) and
\(F(x+1)\), excluding zeros of the denominator. Both displayed Gamma
expressions are finite and nonzero for real \(x\ge0\). On real domains,
nonzero functions of period one also multiply solutions, so this is not a
uniqueness claim up to constants.

This row shares the exact forward-quotient certificate and grading contract
with UK relay 10. The distinct answer kind interprets \(C\) as nonzero,
accepts both printed forms and their nonzero constant multiples, and rejects
additive shifts. Ordinary indefinite grading is unchanged. The catalog
stores \(C=1\) and repairs the OCR Gamma argument to \(x+2026/2025\).

## Final answer

\[
C\cdot 2025^{x}\Gamma\Bigl(x+\dfrac{2026}{2025}\Bigr)
=
C\cdot 2025^{x}\Bigl(x+\dfrac{1}{2025}\Bigr)\Gamma\Bigl(x+\dfrac{1}{2025}\Bigr).
\]

The multiplicative constant satisfies \(C\ne0\).

## SymPy self-check

`verify/pack_multiplicative.py` checks the source's forward quotient by the
Gamma recurrence. `verify/pack_multiplicative_check.py` exercises this id and
UK relay 10 through the same certificate and turn grading, including both
printed forms, constant multiples, wrong Gamma arguments, additive shifts,
zero and undefined answers, and the ordinary additive-constant regression.
`solutions/self_check.py` retains its earlier Gamma-recurrence diagnostic.
