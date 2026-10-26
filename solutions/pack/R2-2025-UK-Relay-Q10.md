# R2-2025-UK-Relay-Q10

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (p.3, relay 10)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (p.3, relay 10)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is `verify: sympy`, with kind `discrete_multiplicative`.

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

Here \(C\ne0\); zero cannot be an antiderivative because its forward quotient
is undefined. The identities hold wherever both \(F(x)\) and \(F(x+1)\) are
defined and \(F(x)\ne0\). In particular, the displayed Gamma expressions are
finite and nonzero for real \(x\ge0\). No claim of uniqueness up to a constant
is needed: on a real domain, a nonzero function of period one can multiply a
solution without changing its forward quotient.

The distinct answer kind checks the source-defined quotient exactly and
interprets \(C\) as nonzero only for this kind. It accepts constant multiples
of either printed form, rejects additive shifts, and leaves ordinary
indefinite integrals under their original additive-constant rule. The catalog
stores the representative with \(C=1\), and repairs the earlier OCR argument
\((x+2026)/2025\) to \(x+2026/2025\).

## Final answer

\[
C\cdot 2025^{x}\Gamma\Bigl(x+\dfrac{2026}{2025}\Bigr)
=
C\cdot 2025^{x}\Bigl(x+\dfrac{1}{2025}\Bigr)\Gamma\Bigl(x+\dfrac{1}{2025}\Bigr).
\]

The multiplicative constant satisfies \(C\ne0\).

## SymPy self-check

`verify/pack_multiplicative.py` applies \(\Gamma(w+1)=w\Gamma(w)\) with
`expand_func` and cancels the resulting forward quotient to
\(2025x+2026\). The gate uses that certificate for this answer kind.
`verify/pack_multiplicative_check.py` checks both printed forms, nonzero
constant multiples, a nonzero periodic multiple, and grading through the
turn contract. It rejects additive shifts, the wrong Gamma argument, a bare
\(2025^x\), zero, undefined values, and a changed source factor. It also checks
that ordinary indefinite grading still accepts additive constants and rejects
nontrivial multiplicative constants. `solutions/self_check.py` retains its
earlier Gamma-recurrence diagnostic.
