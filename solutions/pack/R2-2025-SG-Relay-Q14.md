# R2-2025-SG-Relay-Q14

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf`, PDF page 4, relay 14.
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The original problem page has been visually checked. The catalog's `answer_source_pdf: derived_verified` is retained; this proof does not claim agreement with an unavailable Singapore mark scheme.

## Problem

\[
\int_{1}^{\infty}\sum_{k=1}^{\infty}\frac{1}{k+1}\left\lfloor\frac{k+1}{\{x\}}\right\rfloor^{-\lfloor x\rfloor}\,dx.
\]

## Solution

Write \(x=n+t\) with an integer \(n\geq 1\) and \(t\in(0,1)\). Integer endpoints do not affect the integral. The fractional part is \(t\), and the inner power is \(J^{-n}\) where \(J=\lfloor(k+1)/t\rfloor\geq k+1\geq 2\). Every term is positive, so Tonelli's theorem permits both rearrangements of sums and integrals. The geometric series is

\[
\sum_{n\geq 1}J^{-n}=\frac{1}{J-1}.
\]

Set \(M=k+1\). The factor \(1/(k+1)\) is \(1/M\), and the integral over \(t\) is

\[
\frac{1}{M}\int_{0}^{1}\frac{dt}{\lfloor M/t\rfloor-1}.
\]

On the interval where \(\lfloor M/t\rfloor=j\), namely \(t\in(M/(j+1),M/j]\) for each integer \(j\geq M\), the length is \(M/(j(j+1))\). The integral becomes

\[
\sum_{j\geq M}\frac{1}{j(j-1)(j+1)}.
\]

Summing over \(M\geq 2\) counts the pair \((j,M)\) once for each \(M\) from \(2\) to \(j\), which is \(j-1\) times:

\[
\sum_{j\geq 2}\frac{j-1}{j(j-1)(j+1)}=\sum_{j\geq 2}\frac{1}{j(j+1)}=\frac12.
\]

## Final answer

\[
\frac{1}{2}.
\]

## SymPy self-check

`verify/pack_hard_floor.py` preserves the literal infinite `Sum` in the transcript. Its certificate first matches that sum, the summation range, the bound index, and both integration limits. SymPy then checks the integer translation of the floor, the substituted body, the convergent geometric sum for every integer \(J\geq2\), the exact floor-interval lengths, their multiplicities, and the final telescoping sum. Unsupported sums are not accepted by this certificate.
