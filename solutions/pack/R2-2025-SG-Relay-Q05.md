# R2-2025-SG-Relay-Q05

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 5). The same integral is relay 17 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 17)
- Worked source: derived in this note.
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

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q05`. SymPy checks the same floor identity and zeta value as the UK relay 17 note.
