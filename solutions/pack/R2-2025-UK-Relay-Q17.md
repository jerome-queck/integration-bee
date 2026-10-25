# R2-2025-UK-Relay-Q17

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 17)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 17)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{1}^{\infty}\frac{1}{\lfloor x+\lfloor x\rfloor\rfloor^{2}}\,dx.
\]

## Solution

Write \(x=n+f\) with an integer \(n\ge 1\) and \(f\in[0,1)\). Then \(\lfloor x\rfloor=n\) and
\[
\lfloor x+\lfloor x\rfloor\rfloor=\lfloor n+f+n\rfloor=2n.
\]
On each interval \([n,n+1)\) the integrand is \(1/(4n^{2})\). Therefore
\[
\sum_{n=1}^{\infty}\frac{1}{4n^{2}}=\frac14\zeta(2)=\frac{\pi^{2}}{24}.
\]
The mark scheme prints \(\pi^{2}/24\).

## Final answer

\[
\frac{\pi^{2}}{24}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q17`. SymPy checks \(\lfloor 2n\rfloor=2n\) and \(\lfloor 2n+1/3\rfloor=2n\) for an integer symbol \(n\), and sums \(\sum 1/(4m^{2})\).
